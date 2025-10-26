from __future__ import annotations

import urllib.parse
import urllib.request

from ..core.message import Request, Response
from ..core.status import Status


class StdLibClient:
    """
    HTTP client implementation using Python's urllib.request.

    This is just an HttpHandler function that makes actual HTTP calls
    instead of processing business logic.
    """

    def __call__(self, request: Request) -> Response:
        try:
            # Convert http4py Request to urllib Request
            url = str(request.uri)

            # Prepare headers
            headers = request.headers.copy()

            # Prepare body data
            body_data = None
            if request.body.bytes:
                body_data = request.body.bytes
                if "Content-Length" not in headers:
                    headers["Content-Length"] = str(len(body_data))

            # Create urllib request
            urllib_request = urllib.request.Request(
                url=url, data=body_data, headers=headers, method=request.method.name
            )

            # Make the HTTP call
            with urllib.request.urlopen(urllib_request) as urllib_response:
                # Convert urllib response to http4py Response
                status_code = urllib_response.getcode()
                response_headers = dict(urllib_response.headers.items())
                response_body = urllib_response.read()

                # Find matching Status object
                status = Status.from_code(status_code)

                # Create http4py Response
                response = Response(status).headers_(response_headers)
                if response_body:
                    response = response.body_(response_body)

                return response

        except urllib.error.HTTPError as e:
            # Handle HTTP errors (4xx, 5xx) as valid responses
            status = Status.from_code(e.code)
            response_headers = dict(e.headers.items()) if e.headers else {}
            response_body = e.read() if hasattr(e, "read") else b""

            response = Response(status).headers_(response_headers)
            if response_body:
                response = response.body_(response_body)

            return response

        except Exception as e:
            # Handle network/connection errors as 500
            error_body = f"Client Error: {str(e)}"
            return Response(Status.INTERNAL_SERVER_ERROR).body_(error_body)
