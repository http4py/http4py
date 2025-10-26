from __future__ import annotations

from dataclasses import dataclass

from ..http import Filter, HttpHandler
from ..message import Request, Response


@dataclass(frozen=True)
class DebuggingFilter(Filter):
    def __call__(self, next: HttpHandler) -> HttpHandler:
        def decorated_handler(request: Request) -> Response:
            print(f"→ {request.method.name} {request.uri}")
            response = next(request)
            print(f"← {response.status.code}")
            return response
        return decorated_handler
