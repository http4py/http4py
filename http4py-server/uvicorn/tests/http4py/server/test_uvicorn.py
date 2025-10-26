from __future__ import annotations

from http4py.core import Request, Response
from http4py.core.status import OK
from http4py.server_uvicorn import Uvicorn


def test_uvicorn_server_creation() -> None:
    def handler(request: Request) -> Response:
        return Response(OK).body_("Hello World")

    server = Uvicorn(8080).serve(handler)
    assert server.port() == 8080


def test_uvicorn_default_port() -> None:
    def handler(request: Request) -> Response:
        return Response(OK).body_("Hello World")

    server = Uvicorn().serve(handler)
    assert server.port() == 8080
