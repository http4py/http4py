from __future__ import annotations

from http4py.core import Request, Response
from http4py.core.status import OK
from http4py.server_asgi import AsgiAdapter, StandardAsgiAdapter, asgi_adapter


def test_standard_asgi_adapter() -> None:
    def handler(request: Request) -> Response:
        return Response(OK).body_("Hello World")

    adapter = StandardAsgiAdapter()
    app = adapter.to_asgi(handler)
    assert callable(app)


def test_asgi_adapter_function() -> None:
    def handler(request: Request) -> Response:
        return Response(OK).body_("Hello World")

    app = asgi_adapter(handler)
    assert callable(app)


def test_asgi_adapter_interface() -> None:
    adapter = StandardAsgiAdapter()
    assert isinstance(adapter, AsgiAdapter)
