from __future__ import annotations

from typing import Optional
import requests

from http4py.core.message import Request, Response
from http4py.core.status import Status


class RequestsClient:
    def __init__(self, session: requests.Session | None = None, timeout: float | None = None):
        self._session = session or requests.Session()
        self._timeout = timeout

    def __call__(self, request: Request) -> Response:
        try:
            url = str(request.uri)
            method = request.method.name
            headers = {}
            for name, value in request.headers:
                if value is not None:
                    headers[name] = value

            data = None
            if request.body.bytes:
                data = request.body.bytes
                has_content_length = any(name.lower() == "content-length" for name, _ in request.headers)
                if not has_content_length:
                    headers["Content-Length"] = str(len(data))

            response = self._session.request(
                method=method, url=url, headers=headers, data=data, timeout=self._timeout, allow_redirects=True
            )

            status = Status.from_code(response.status_code)
            response_body = response.content

            http4py_response = Response(status).headers_([(name, value) for name, value in response.headers.items()])
            if response_body:
                http4py_response = http4py_response.body_(response_body)

            return http4py_response

        except requests.exceptions.RequestException as e:
            error_body = f"Request Error: {str(e)}"
            return Response(Status.INTERNAL_SERVER_ERROR).body_(error_body)
        except Exception as e:
            error_body = f"Client Error: {str(e)}"
            return Response(Status.INTERNAL_SERVER_ERROR).body_(error_body)
