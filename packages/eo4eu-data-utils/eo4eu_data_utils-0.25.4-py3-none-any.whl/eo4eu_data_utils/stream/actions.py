import logging
from pathlib import Path
from eo4eu_base_utils import if_none
from eo4eu_base_utils.unify import overlay
from eo4eu_base_utils.typing import Callable, Any, List, Dict, Iterator

from .model import Action, Data
from .logs import default_logger
from ..metainfo import DSMetainfo


def _no_op(*args, **kwargs):
    pass


def _make_default_err_callback(name: str):
    return lambda item, e: default_logger.warning(
        f"Failed to {name} \"{item}\": {e}"
    )


class NoOp(Action):
    def __init__(self):
        pass

    def act(self, input: Data) -> Data:
        return input


class Apply(Action):
    def __init__(self, func: Callable[[Data],Data]):
        self._func = func

    def act(self, input: Data) -> Data:
        return self._func(input)


class Map(Action):
    def __init__(
        self,
        map_func: Callable[[Any],List[Any]],
        iter_func: Callable[[Data],Iterator[Any]]|None = None,
        err_callback: Callable[[Any, Exception],Any]|None = None,
        name: str = "map"
    ):
        self._map_func = map_func
        self._iter_func = if_none(iter_func, lambda data: data.passed)
        self._err_callback = if_none(err_callback, _make_default_err_callback(name))

    def act(self, input: Data) -> Data:
        passed, failed = [], []
        for item in self._iter_func(input):
            try:
                result = self._map_func(item)
                if isinstance(result, list):
                    passed.extend(result)
                else:
                    passed.append(result)
            except Exception as e:
                self._err_callback(item, e)
                failed.append(item)

        return input.but(passed = passed, failed = failed)


# This is a Callable[[Any],List[Any]]
class TransferMap:
    def __init__(
        self,
        dst_func: Callable[[Any],Any],
        transfer_func: Callable[[Any,Any],List[Any]],
        logger: logging.Logger|None = None,
        name: str = "Transferring",
    ):
        self._dst_func = dst_func
        self._transfer_func = transfer_func
        self._logger = if_none(logger, default_logger)
        self._name = name
        self._spaces = " " * (len(self._name) - 3)

    def __call__(self, src: Any) -> List[Any]:
        self._logger.info(f"{self._name} {src}")
        dst = self._dst_func(src)
        out_paths = self._transfer_func(src, dst)
        if not isinstance(out_paths, list):
            out_paths = [out_paths]

        head, tail = out_paths[0], out_paths[1:]
        self._logger.info(f"{self._spaces} to {head}")
        for path in tail:
            self._logger.info(f"{self._spaces}    {path}")

        return out_paths


# This is a Callable[[Any],List[Any]]
class FilterMap:
    def __init__(self, predicate: Callable[[Any],bool]):
        self._predicate = predicate

    def __call__(self, src: Any) -> List[Any]:
        if self._predicate(src):
            return [src]
        else:
            raise ValueError(f"Item \"{src}\" failed to satisfy predicate")


class Overlay(Action):
    def __init__(self, kwargs: Dict[str,Any]):
        self._kwargs = kwargs

    def act(self, input: Data) -> Data:
        return input.but(kwargs = overlay(input.kwargs, self._kwargs))


class Source(Action):
    def __init__(
        self,
        source: Callable[[],Data],
        err_callback: Callable[[Any, Exception],Any]|None = None
    ):
        self._source = source
        self._err_callback = if_none(err_callback, _make_default_err_callback("source"))

    def act(self, input: Data) -> Data:
        result = Data.empty()
        try:
            result.passed = self._source()
        except Exception as e:
            self._err_callback(self._source.__name__, e)

        return input.merge(result)


class Switch(Action):
    def __init__(
        self,
        cases: List[tuple[Callable[[Any],bool],Action]],
        iter_func: Callable[[Data],Iterator[Any]]|None = None,
        err_callback: Callable[[Any, Exception],Any]|None = None
    ):
        self._cases = cases
        self._iter_func = if_none(iter_func, lambda data: data.passed)
        self._err_callback = if_none(err_callback, _make_default_err_callback("switch"))

    def act(self, input: Data) -> Data:
        groups = [[] for _ in self._cases]
        result = input
        for item in self._iter_func(input):
            try:
                for idx, (predicate, _) in enumerate(self._cases):
                    if predicate(item):
                        groups[idx].append(item)
                        break
            except Exception as e:
                self._err_callback(item, e)
                failed.append(item)

        for (_, action), data in zip(self._cases, groups):
            try:
                result = result.merge(action.act(data))
            except Exception as e:
                self._err_callback(data, e)

        return result


class Report(Action):
    def __init__(
        self,
        trigger_func: Callable[[Data],bool]|None = None,
        report_func: Callable[[Data],None]|None = None,
    ):
        self._trigger_func = if_none(trigger_func, lambda data: True)
        self._report_func = if_none(report_func, lambda data: print(data))

    def act(self, input: Data) -> Data:
        try:
            if self._trigger_func(input):
                self._report_func(input)
        except Exception as e:
            default_logger.warning(f"Failed to report: {e}")

        return input


class Rename(Action):
    def __init__(
        self,
        method: Callable[[List[Path]],List[Path]],
        err_callback: Callable[[Any, Exception],Any]|None = None
    ):
        self._method = method
        self._err_callback = if_none(err_callback, _make_default_err_callback("rename"))

    def act(self, input: Data) -> Data:
        try:
            old_names = [
                pathspec.name for pathspec in input.passed
            ]
            new_names = self._method(old_names)
            if len(new_names) != len(old_names):
                raise ValueError(
                    f"Method \"{self._method.__name__}\" returned {len(new_names)} paths, "
                    f"expected {len(old_names)}"
                )

            return input.but(passed = [
                (item.but(name = name) if name is not None else item)
                for item, name in zip(input.passed, new_names)
            ])
        except Exception as e:
            self._err_callback(input, e)

        return input


class FillMetainfo(Action):
    def __init__(
        self,
        metainfo: DSMetainfo,
        distance: Callable[[str,Path],float],
        method: Callable[[List[List[float]]],List[int]],
        default: Callable[[Any],Dict]|None = None,
        product_id: Callable[[Dict],str]|str = "id",
        path_getter: Callable[[Any],Path]|None = None,
        meta_setter: Callable[[Any,Dict],Any]|None = None,
        err_callback: Callable[[Any, Exception],Any]|None = None
    ):
        if isinstance(product_id, str):
            self._product_id = lambda product: product[product_id]
        else:
            self._product_id = product_id

        self._metainfo = metainfo
        self._distance = distance
        self._method = method
        self._default = if_none(default, lambda pathspec: {"id": str(pathspec.name)})
        self._path_getter = if_none(path_getter, lambda pathspec: pathspec.path)
        self._meta_setter = if_none(meta_setter, lambda pathspec, meta: pathspec.but(
            meta = overlay(pathspec.meta, {"meta": meta})
        ))
        self._err_callback = if_none(err_callback, _make_default_err_callback("fill metainfo for"))

    def _default_result(self, input: Data) -> Data:
        return input.but(passed = [
            self._meta_setter(item, self._default(item))
            for item in input
        ])

    def act(self, input: Data) -> Data:
        try:
            if len(self._metainfo.products) <= 0:
                raise ValueError(f"Given metainfo has no products")

            distance_matrix = [
                [
                    self._distance(self._product_id(product), self._path_getter(item))
                    for product in self._metainfo.products
                ]
                for item in input
            ]
            matches = self._method(distance_matrix)
            if len(matches) != input.len():
                raise ValueError(
                    f"Method \"{self._method.__name__}\" returned {len(matches)} matches, "
                    f"expected {input.len()}"
                )

            result = []
            for item, match_idx in zip(input, matches):
                meta = None
                if match_idx < 0:
                    meta = self._default(item)
                else:
                    try:
                        meta = self._metainfo.products[match_idx]
                    except Exception as e:
                        self._err_callback(item, e)
                        meta = self._default(item)

                result.append(self._meta_setter(item, meta))

            return input.but(passed = result)
        except Exception as e:
            self._err_callback(input, e)

        return self._default_result(input)
