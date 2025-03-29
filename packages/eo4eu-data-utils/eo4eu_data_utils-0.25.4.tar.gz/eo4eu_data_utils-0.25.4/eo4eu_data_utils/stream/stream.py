import logging
import functools
import mimetypes
from pathlib import Path
from eo4eu_base_utils import if_none
from eo4eu_base_utils.unify import overlay
from eo4eu_base_utils.typing import Any, List, Self, Callable

from .actions import (
    NoOp,
    Apply,
    Map,
    TransferMap,
    FilterMap,
    Source,
    Switch,
    Report,
    Rename,
    FillMetainfo,
)
from .drivers import Downloader, Uploader, Lister, LocalDriver
from .model import Data, Action, PathSpec
from .logs import default_logger
from ..metainfo import DSMetainfo
from ..helpers import (
    unsafe_unpack,
    default_rename_methods,
    default_fill_meta_methods,
    default_string_distances,
)


class Stream(Action):
    def __init__(self, actions: List[Action]|None = None):
        self._actions = if_none(actions, [])

    def act(self, input: Data) -> Data:
        result = input
        for action in self._actions:
            result = action.act(result)
        return result

    def exec(self) -> Data:
        return self.act(Data.empty())

    def then(self, action: Action) -> Self:
        self._actions.append(action)
        return self

    def then_if(self, if_true: bool, action: Action) -> Self:
        if if_true:
            return self.then(action)
        return self

    def apply(self, *args, **kwargs) -> Self:
        return self.then(Apply(*args, **kwargs))

    def map(self, *args, **kwargs) -> Self:
        return self.then(Map(*args, **kwargs))

    def source(self, *args, **kwargs) -> Self:
        return self.then(Source(*args, **kwargs))

    def ls(
        self,
        lister: Lister|None = None,
        src: Path|None = None,
        **kwargs
    ) -> Self:
        lister = if_none(lister, LocalDriver())
        src = if_none(src, Path(""))
        return self.then(Source(
            source = lambda: lister.ls(src),
            **kwargs
        ))

    def raw(self, items: List[Any], **kwargs) -> Self:
        return self.then(Source(
            source = lambda: items,
            **kwargs
        ))

    def transfer(
        self,
        dst_func: Callable[[PathSpec],PathSpec],
        transfer_func: Callable[[PathSpec,PathSpec],List[PathSpec]],
        logger: logging.Logger|None = None,
        transferring: str = "Transferring",
        transfer: str = "transfer",
        **kwargs
    ) -> Self:
        logger = if_none(logger, default_logger)

        return self.map(**{
            "map_func": TransferMap(
                dst_func = dst_func,
                transfer_func = transfer_func,
                logger = logger,
                name = transferring
            ),
            "err_callback": lambda item, e: logger.warning(f"Failed to {transfer} {item}: {e}"),
        } | kwargs)

    def download(self, downloader: Downloader, dst: Path, **kwargs) -> Self:
        return self.transfer(**({
            "dst_func":      _get_default_dst_func(dst),
            "transfer_func": functools.partial(_download_func, downloader = downloader),
            "transferring":  "Downloading",
            "transfer":      "download",
        } | kwargs))

    def upload(self, uploader: Uploader, dst: Path, **kwargs) -> Self:
        return self.transfer(**({
            "dst_func":      _get_default_dst_func(dst),
            "transfer_func": functools.partial(_upload_func, uploader = uploader),
            "transferring":  "Uploading",
            "transfer":      "upload",
        } | kwargs))

    def move(self, uploader: Uploader, dst: Path, **kwargs) -> Self:
        return self.transfer(**({
            "dst_func":      _get_default_dst_func(dst),
            "transfer_func": _move_func,
            "transferring":  "Moving",
            "transfer":      "move",
        } | kwargs))

    def unpack(self, dst: Path, **kwargs) -> Self:
        return self.transfer(**({
            "dst_func":      _get_default_dst_func(dst),
            "transfer_func": _unpack_func,
            "transferring":  "Unpacking",
            "transfer":      "unpack",
        } | kwargs))

    def filter(
        self,
        predicate: Callable[[Any],bool],
        drop_failed: bool = True,
        **kwargs
    ) -> Self:
        result = self.map(**({
            "map_func": FilterMap(predicate)
        } | kwargs))
        if drop_failed:
            return result.drop_failed()
        else:
            return result

    def switch(self, *args, **kwargs) -> Self:
        return self.then(Switch(*args, **kwargs))

    def ifelse(
        self,
        predicate: Callable[[Any],bool],
        if_action: Action,
        else_action: Action,
        **kwargs
    ) -> Self:
        return self.switch(**{
            "cases": [
                (predicate, if_action),
                (lambda item: True, else_action),
            ],
        } | kwargs)

    def branch(
        self,
        predicate: Callable[[Any],bool],
        action: Action,
        **kwargs
    ) -> Self:
        return self.ifelse(predicate, action, NoOp())

    def report(self, *args, **kwargs) -> Self:
        return self.then(Report(*args, **kwargs))

    def warn(
        self,
        func: Callable[[tuple[int,int]],None]|str = "Failed: {}/{} items",
        **kwargs
    ) -> Self:
        report_func = func
        if isinstance(func, str):
            report_func = lambda failed, total: default_logger.warning(
                func.format(failed, total)
            )

        return self.report(**({
            "trigger_func": lambda data: data.any_failed(),
            "report_func":  lambda data: report_func(*data.warn_stats())
        } | kwargs))

    def drop_failed(self) -> Self:
        return self.apply(lambda data: data.but(failed = []))

    def rename(
        self,
        method: Callable[[List[Path]],List[Path]]|str = "shortest_unique",
        **kwargs
    ) -> Self:
        if isinstance(method, str):
            method = default_rename_methods.get(
                method, default_rename_methods["shortest_unique"]
            )

        return self.then(Rename(**({
            "method": method,
        } | kwargs)))

    def do(
        self,
        func: Callable[[],None],
        *args,
        **kwargs
    ):
        def _sub_func(input, *args, **kwargs):
            func(*args, **kwargs)
            return input

        return self.apply(
            func = functools.partial(_sub_func, *args, **kwargs)
        )

    def fill_metainfo(
        self,
        metainfo: DSMetainfo,
        distance: Callable[[str,Path],float]|str = "group_distance",
        method: Callable[[List[List[float]]],List[int]]|str = "unique_sort_match",
        **kwargs
    ):
        if isinstance(distance, str):
            distance = default_string_distances.get(
                distance, default_string_distances["group_distance"]
            )
        if isinstance(method, str):
            method = default_fill_meta_methods.get(
                method, default_fill_meta_methods["unique_sort_match"]
            )

        return self.then(FillMetainfo(**({
            "metainfo": metainfo,
            "distance": distance,
            "method":   method,
        } | kwargs)))


def _base_default_dst_func(src: PathSpec, dst: Path) -> PathSpec:
    return src.but(
        name = src.name,
        path = dst.joinpath(src.name)
    )


def _get_default_dst_func(dst: Path|str) -> Callable[[PathSpec],PathSpec]:
    return functools.partial(_base_default_dst_func, dst = Path(dst))


def _move_func(src: PathSpec, dst: PathSpec) -> PathSpec:
    src.path.rename(dst.path)
    return dst


def _download_func(src: PathSpec, dst: PathSpec, downloader: Downloader) -> PathSpec:
    downloader.download(src.path, dst.path)
    return dst


def _upload_func(src: PathSpec, dst: PathSpec, uploader: Uploader) -> PathSpec:
    uploader.upload(src.path, dst.path)
    return dst


def _unpack_func(src: PathSpec, dst: PathSpec) -> List[PathSpec]:
    if mimetypes.guess_type(src.path)[0] in [
        "application/x-tar",
        "application/zip",
    ]:
        return [
            src.but(
                name = out_path.relative_to(dst.path.parent),
                path = out_path
            )
            for out_path in unsafe_unpack(src.path, dst.path)
        ]
    else:
        return [src]
