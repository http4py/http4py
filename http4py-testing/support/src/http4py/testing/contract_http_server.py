from __future__ import annotations

import socket
import threading
import time
from abc import ABC, abstractmethod

import requests

from http4py.core import Request, Response
from http4py.core.method import GET, POST
from http4py.core.status import OK, CREATED
from http4py.routing import route, routes
from http4py.server import Http4pyServer, ServerConfig


def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.listen(1)
        return s.getsockname()[1]


def hello_handler(request: Request) -> Response:
    return Response(OK).body_("Hello World").header_("Content-Type", "text/plain")


def echo_handler(request: Request) -> Response:
    body_text = request.body.text
    return Response(CREATED).body_(f"Received: {body_text}").header_("Content-Type", "text/plain")


def header_handler(request: Request) -> Response:
    response = Response(OK).header_("Content-Type", "application/json")
    
    # Echo back all request headers as response headers with "Echo-" prefix
    for name, value in request.headers:
        response = response.header_(f"Echo-{name}", value)
    
    return response.body_("{}")


def create_test_app():
    return routes(
        route("/hello").bind(GET).to(hello_handler),
        route("/echo").bind(POST).to(echo_handler),
        route("/headers").bind(GET).to(header_handler)
    )


class HttpServerContract(ABC):
    @abstractmethod
    def create_server_config(self, port: int) -> ServerConfig:
        pass

    def _start_test_server(self):
        config = self.create_server_config(0)
        server = config.serve(create_test_app()).start()

        server_thread = threading.Thread(target=server.block, daemon=True)
        server_thread.start()
        time.sleep(0.1)

        return server

    def test_get_request_handling(self) -> None:
        server = self._start_test_server()
        try:
            response = requests.get(f"http://localhost:{server.port()}/hello", timeout=5)
            assert response.status_code == 200
            assert response.text == "Hello World"
            assert response.headers["Content-Type"] == "text/plain"
        finally:
            server.stop()

    def test_post_request_with_body(self) -> None:
        server = self._start_test_server()
        try:
            response = requests.post(
                f"http://localhost:{server.port()}/echo",
                data="test data",
                headers={"Content-Type": "text/plain"},
                timeout=5
            )
            assert response.status_code == 201
            assert response.text == "Received: test data", f"Expected 'Received: test data', got {response.text!r}"
        finally:
            server.stop()

    def test_header_processing(self) -> None:
        server = self._start_test_server()
        try:
            request_headers = {
                "Authorization": "Bearer token123",
                "X-Custom-Header": "test-value",
                "X-API-Key": "secret123"
            }
            
            response = requests.get(
                f"http://localhost:{server.port()}/headers",
                headers=request_headers,
                timeout=5
            )
            
            assert response.status_code == 200
            
            # Check that all request headers are echoed back with "Echo-" prefix
            for name, value in request_headers.items():
                echo_header_name = f"Echo-{name}"
                assert echo_header_name in response.headers, f"Missing echoed header: {echo_header_name}"
                assert response.headers[echo_header_name] == value, f"Header value mismatch for {echo_header_name}"
        finally:
            server.stop()
