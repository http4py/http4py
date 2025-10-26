from __future__ import annotations

from dataclasses import dataclass

from ..core.http import Filter, HttpHandler
from ..core.message import Request, Response


@dataclass(frozen=True)
class DebuggingFilter(Filter):
    def __call__(self, fn: HttpHandler) -> HttpHandler:
        def decorated_handler(request: Request) -> Response:
            print(f"→ {request.method.name} {request.uri}")
            response = fn(request)
            print(f"← {response.status.code}")
            return response

        return decorated_handler
