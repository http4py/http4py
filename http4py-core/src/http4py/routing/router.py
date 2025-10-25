from __future__ import annotations

from dataclasses import dataclass

from .route import _RouteDefinition
from ..core.message import Request, Response
from ..core.status import Status


@dataclass(frozen=True)
class RoutingHttpHandler:
    routes: list[_RouteDefinition]

    def __call__(self, request: Request) -> Response:
        for route_def in self.routes:
            if self._matches(request, route_def):
                return route_def.handler(request)

        return Response(Status.NOT_FOUND).body_("Not Found")

    def _matches(self, request: Request, route_def: _RouteDefinition) -> bool:
        return request.method == route_def.method and request.uri.path == route_def.path


def routes(*route_definitions: _RouteDefinition) -> RoutingHttpHandler:
    return RoutingHttpHandler(list(route_definitions))
