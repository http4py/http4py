from __future__ import annotations

import traceback
from http.server import BaseHTTPRequestHandler
from typing import Any
from urllib.parse import parse_qs, urlparse

from http4py.core import HttpHandler, Request, Response, Method, Uri, Status


class Http4pyRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, http_handler: HttpHandler, *args: Any, **kwargs: Any):
        self.http_handler = http_handler
        super().__init__(*args, **kwargs)

    def do_GET(self) -> None:
        self._handle_request()

    def do_POST(self) -> None:
        self._handle_request()

    def do_PUT(self) -> None:
        self._handle_request()

    def do_DELETE(self) -> None:
        self._handle_request()

    def _handle_request(self) -> None:
        try:
            request = self._convert_to_http4py_request()
            response = self.http_handler(request)
            self._send_http4py_response(response)
        except Exception as e:
            print(f"Error handling request: {e}")
            traceback.print_exc()

            error_body = f"Internal Server Error\n\n{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
            error_response = (
                Response(Status.INTERNAL_SERVER_ERROR).body_(error_body).header_("Content-Type", "text/plain")
            )
            self._send_http4py_response(error_response)

    def _convert_to_http4py_request(self) -> Request:
        method = Method(self.command)

        parsed_url = urlparse(self.path)
        uri = Uri().path_(parsed_url.path)

        if parsed_url.query:
            query_params = parse_qs(parsed_url.query)
            for key, values in query_params.items():
                for value in values:
                    uri = uri.query_(key, value)

        headers = dict(self.headers.items())

        content_length = int(headers.get("content-length", headers.get("Content-Length", 0)))
        body_data = self.rfile.read(content_length) if content_length > 0 else b""

        request = Request(method, uri).headers_(headers)
        if body_data:
            request = request.body_(body_data)

        return request

    def _send_http4py_response(self, response: Response) -> None:
        self.send_response(response.status.code)

        body_bytes = response.body.bytes
        
        # Set Content-Length header if not already set
        if "Content-Length" not in response.headers and body_bytes:
            self.send_header("Content-Length", str(len(body_bytes)))
        elif "Content-Length" not in response.headers:
            self.send_header("Content-Length", "0")

        for name, value in response.headers.items():
            self.send_header(name, value)
            
        # Always close connection to prevent reuse issues
        self.send_header("Connection", "close")
        self.end_headers()

        if body_bytes:
            self.wfile.write(body_bytes)
