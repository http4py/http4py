from __future__ import annotations

from dataclasses import dataclass

from ..core.http import HttpHandler
from ..core.method import Method


@dataclass(frozen=True)
class Route:
    path: str

    def bind(self, method: Method) -> _PathMethod:
        return _PathMethod(self.path, method)


@dataclass(frozen=True)
class _PathMethod:
    path: str
    method: Method

    def to(self, handler: HttpHandler) -> _RouteDefinition:
        return _RouteDefinition(self.path, self.method, handler)


@dataclass(frozen=True)
class _RouteDefinition:
    path: str
    method: Method
    handler: HttpHandler


def route(path: str) -> Route:
    return Route(path)
