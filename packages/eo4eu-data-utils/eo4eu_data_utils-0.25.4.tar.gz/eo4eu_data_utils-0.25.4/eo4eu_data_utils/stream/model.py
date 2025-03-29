from pathlib import Path
from pprint import pformat
from abc import ABC, abstractmethod
from eo4eu_base_utils.unify import overlay
from eo4eu_base_utils.typing import Self, Any, List, Dict, Iterator

from ..helpers import format_list


class PathSpec:
    def __init__(self, name: Path, path: Path, meta: dict[str,Any]):
        self.name = Path(name)
        self.path = Path(path)
        self.meta = meta

    def but(self, **kwargs) -> Self:
        return PathSpec(**overlay(
            {"name": self.name, "path": self.path, "meta": self.meta},
            kwargs
        ))

    def __repr__(self) -> str:
        # return f"path: \"{self.path}\", name: \"{self.name}\""
        try:
            name_is_in_path = self.path.match(self.name)
            if name_is_in_path:
                name = str(self.name)
                start = str(self.path)[::-1][len(name):][::-1]
                return f"{start}({name})"
            else:
                return str(self.path)
        except Exception as e:
            return f"[Failed to format path: {e}]"


class Data:
    def __init__(self, passed: List[Any], failed: List[Any], kwargs: Dict[str,Any]):
        self.passed = passed
        self.failed = failed
        self.kwargs = kwargs

    @classmethod
    def empty(self) -> Self:
        return Data([], [], {})

    def but(self, **kwargs) -> Self:
        return Data(**({
            "passed": self.passed,
            "failed": self.failed,
            "kwargs": self.kwargs,
        } | kwargs))

    def __iter__(self) -> Iterator[Any]:
        for item in self.passed:
            yield item

    def iter_all(self) -> Iterator[Any]:
        for passed in self.passed:
            yield passed
        for failed in self.failed:
            yield failed

    def merge(self, other: Self) -> Self:
        return Data(
            passed = self.passed + other.passed,
            failed = self.failed + other.failed,
            kwargs = overlay(self.kwargs, other.kwargs)
        )

    def len(self) -> int:
        return len(self.passed)

    def stats(self) -> tuple[int,int]:
        return (len(self.passed), len(self.failed))

    def warn_stats(self) -> tuple[int,int]:
        return (len(self.failed), len(self.passed) + len(self.failed))

    def any_failed(self) -> bool:
        return len(self.failed) > 0

    def __repr__(self) -> str:
        return "\n".join([
            format_list("passed: ", self.passed),
            format_list("failed: ", self.failed),
            f"kwargs: {pformat(self.kwargs)}",
        ])



class Action(ABC):
    @abstractmethod
    def act(self, input: Data) -> Data:
        return input
