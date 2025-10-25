from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any

from http4py.core import HttpHandler, Request
from http4py.core.method import Method
from http4py.core.uri import Uri

AsgiApp = Callable[
    [dict[str, Any], Callable[[], Awaitable[dict[str, Any]]], Callable[[dict[str, Any]], Awaitable[None]]],
    Awaitable[None],
]


class AsgiAdapter(ABC):
    @abstractmethod
    def to_asgi(self, handler: HttpHandler) -> AsgiApp:
        pass


class StandardAsgiAdapter(AsgiAdapter):
    def to_asgi(self, handler: HttpHandler) -> AsgiApp:
        async def asgi_app(
            scope: dict[str, Any],
            receive: Callable[[], Awaitable[dict[str, Any]]],
            send: Callable[[dict[str, Any]], Awaitable[None]],
        ) -> None:
            if scope["type"] != "http":
                return

            method = Method(scope["method"])

            path = scope["path"]
            query_string = scope.get("query_string", b"").decode("utf-8")
            if query_string:
                path = f"{path}?{query_string}"

            uri = Uri.of(path)

            request = Request(method, uri)

            headers: dict[str, str] = {}
            for name_bytes, value_bytes in scope.get("headers", []):
                name = name_bytes.decode("latin1")
                value = value_bytes.decode("latin1")
                headers[name] = value

            request = request.headers_(headers)

            body_parts: list[bytes] = []
            while True:
                message = await receive()
                if message["type"] == "http.request":
                    body_parts.append(message.get("body", b""))
                    if not message.get("more_body", False):
                        break
                elif message["type"] == "http.disconnect":
                    return

            body = b"".join(body_parts)
            if body:
                request = request.body_(body)

            response = handler(request)

            await send(
                {
                    "type": "http.response.start",
                    "status": response.status.code,
                    "headers": [
                        [name.encode("latin1"), value.encode("latin1")] for name, value in response.headers.items()
                    ],
                }
            )

            await send(
                {
                    "type": "http.response.body",
                    "body": response.body.bytes,
                }
            )

        return asgi_app


def asgi_adapter(http_handler: HttpHandler) -> AsgiApp:
    return StandardAsgiAdapter().to_asgi(http_handler)
