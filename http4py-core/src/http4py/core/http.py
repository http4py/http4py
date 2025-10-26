from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass

from .message import Request, Response

HttpHandler = Callable[[Request], Response]


@dataclass(frozen=True)
class Filter(ABC):
    @abstractmethod
    def __call__(self, handler: HttpHandler) -> HttpHandler:
        pass

    def then(self, handler: HttpHandler) -> HttpHandler:
        return self(handler)

    def thenF(self, next: Filter) -> Filter:
        @dataclass(frozen=True)
        class ComposedFilter(Filter):
            first: Filter
            second: Filter

            def __call__(self, next: HttpHandler) -> HttpHandler:
                return self.first(self.second(next))

        return ComposedFilter(self, next)
