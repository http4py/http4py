from __future__ import annotations

import urllib.parse
import urllib.request

from ..core.message import Request, Response
from ..core.status import Status


class StdLibClient:
    def __call__(self, request: Request) -> Response:
        try:
            url = str(request.uri)

            headers = {}
            for name, value in request.headers:
                headers[name] = value

            body_data = None
            if request.body.bytes:
                body_data = request.body.bytes
                has_content_length = any(name.lower() == "content-length" for name, _ in request.headers)
                if not has_content_length:
                    headers["Content-Length"] = str(len(body_data))

            urllib_request = urllib.request.Request(
                url=url, data=body_data, headers=headers, method=request.method.name
            )

            with urllib.request.urlopen(urllib_request) as urllib_response:
                status_code = urllib_response.getcode()
                response_headers = [(name, value) for name, value in urllib_response.headers.items()]
                response_body = urllib_response.read()

                status = Status.from_code(status_code)

                response = Response.for_status(status).headers_(response_headers)
                if response_body:
                    response = response.body_(response_body)

                return response

        except urllib.error.HTTPError as e:
            status = Status.from_code(e.code)
            response_headers = [(name, value) for name, value in e.headers.items()] if e.headers else []
            response_body = e.read() if hasattr(e, "read") else b""

            response = Response.for_status(status).headers_(response_headers)
            if response_body:
                response = response.body_(response_body)

            return response

        except Exception as e:
            error_body = f"Client Error: {str(e)}"
            return Response(Status.INTERNAL_SERVER_ERROR).body_(error_body)
