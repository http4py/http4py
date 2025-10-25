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

    def handle_one_request(self) -> None:
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ""
                self.request_version = ""
                self.command = ""
                self.send_error(414)
                return
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                return

            request = self._convert_to_http4py_request()
            response = self.http_handler(request)
            self._send_http4py_response(response)
        except Exception as e:
            print(f"Error handling request: {e}")
            traceback.print_exc()

            # Create an error response with the actual exception details
            error_body = f"Internal Server Error\n\n{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
            error_response = (
                Response(Status.INTERNAL_SERVER_ERROR).body_(error_body).header_("Content-Type", "text/plain")
            )
            self._send_http4py_response(error_response)
        finally:
            self.wfile.flush()

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

        content_length = int(headers.get("content-length", 0))
        body_data = self.rfile.read(content_length) if content_length > 0 else b""

        request = Request(method, uri).headers_(headers)
        if body_data:
            request = request.body_(body_data)

        return request

    def _send_http4py_response(self, response: Response) -> None:
        self.send_response(response.status.code)

        for name, value in response.headers.items():
            self.send_header(name, value)
        self.end_headers()

        body_bytes = response.body.bytes
        if body_bytes:
            self.wfile.write(body_bytes)
