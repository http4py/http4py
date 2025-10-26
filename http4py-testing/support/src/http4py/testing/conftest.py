from __future__ import annotations

import threading
from threading import Thread
from time import sleep

import pytest
from http4py.core import Request, Response
from http4py.core.method import GET, POST
from http4py.core.status import OK
from http4py.routing import route, routes
from http4py.server import StdLibServer


def hello_handler(request: Request) -> Response:
    return Response(OK).body_("Hello from http4py server!").header_("Content-Type", "text/plain")


def headers_handler(request: Request) -> Response:
    auth_header = request.headers.get("Authorization", "none")
    custom_header = request.headers.get("X-Custom-Header", "none")
    response_body = f"auth={auth_header},custom={custom_header}"
    return Response(OK).body_(response_body).header_("Content-Type", "text/plain")


def post_users_handler(request: Request) -> Response:
    return Response(OK).body_("POST received").header_("Content-Type", "text/plain")


def create_test_routes():
    return routes(
        route("/").bind(GET).to(hello_handler),
        route("/headers").bind(GET).to(headers_handler),
        route("/api/users").bind(POST).to(post_users_handler),
    )


@pytest.fixture(scope="class")
def test_server():
    sleep(1)
    app = create_test_routes()
    server = StdLibServer(0).serve(app).start()

    server_thread = threading.Thread(target=server.block, daemon=True)
    server_thread.start()

    yield f"http://localhost:{server.port()}"
    server.stop()
