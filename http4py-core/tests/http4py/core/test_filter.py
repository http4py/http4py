from __future__ import annotations

from dataclasses import dataclass

from http4py.core import Request, Response
from http4py.core.http import Filter, HttpHandler
from http4py.core.method import POST
from http4py.core.status import OK


@dataclass(frozen=True)
class ReversingFilter(Filter):
    def __call__(self, next: HttpHandler) -> HttpHandler:
        def decorated(request: Request) -> Response:
            reversed_body = request.body.text[::-1]
            return next(request.body_(reversed_body))

        return decorated


class TestFilter:

    def test_compose_filter(self) -> None:
        def echo(request: Request) -> Response:
            return Response(OK).body_(request.body)

        decorated_handler = ReversingFilter().then(echo)

        response = decorated_handler(Request(POST, "/test").body_("hello"))

        assert response.status == OK
        assert response.body.text == "olleh"

    def test_double_compose_filter(self) -> None:
        def echo(request: Request) -> Response:
            return Response(OK).body_(request.body)

        decorated_handler = ReversingFilter().thenF(ReversingFilter()).then(echo)

        response = decorated_handler(Request(POST, "/test").body_("hello"))

        assert response.status == OK
        assert response.body.text == "hello"
