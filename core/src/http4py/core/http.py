from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .message import Request, Response

HttpHandler = Callable[[Request], Response]
FilterFunction = Callable[[HttpHandler], HttpHandler]


@dataclass(frozen=True)
class Filter:
    filter_fn: FilterFunction

    def __call__(self, handler: HttpHandler) -> HttpHandler:
        return self.filter_fn(handler)

    def thenF(self, next_filter: Filter) -> Filter:
        return Filter(lambda handler: self.filter_fn(next_filter.filter_fn(handler)))

    def then(self, handler: HttpHandler) -> HttpHandler:
        return self.filter_fn(handler)
