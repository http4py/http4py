from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass

from .message import Request, Response

HttpHandler = Callable[[Request], Response]


@dataclass(frozen=True)
class Filter(ABC):
    @abstractmethod
    def __call__(self, fn: HttpHandler) -> HttpHandler:
        pass

    def then(self, fn: HttpHandler) -> HttpHandler:
        return self(fn)

    def thenF(self, fn: Filter) -> Filter:
        @dataclass(frozen=True)
        class ComposedFilter(Filter):
            first: Filter
            second: Filter

            def __call__(self, fn: HttpHandler) -> HttpHandler:
                return self.first(self.second(fn))

        return ComposedFilter(self, fn)
