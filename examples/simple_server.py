#!/usr/bin/env python3
"""
Simple HTTP Server Example using http4py

This example demonstrates:
- Creating a simple HTTP handler function
- Using the @http decorator for fluent API
- Starting a server with StdLib configuration
- Basic request handling and routing
"""

from http4py.core import Request, Response
from http4py.core.method import GET, POST
from http4py.core.status import OK, NOT_FOUND
from http4py.routing import routes, route
from http4py.server import Http4pyServer, StdLib


def main() -> None:
    # Simple single-endpoint server
    def hello_world() -> Http4pyServer:
        def handler(req: Request) -> Response:
            return Response(OK).body_("Hello, World!")

        return StdLib(port=8080).to_server(handler)

    # Server with basic routing
    def multi_route_server() -> Http4pyServer:
        router = routes(
            route("/").bind(GET).to(lambda req: Response(OK).body_("Welcome to http4py!")),
            route("/health").bind(GET).to(lambda req: Response(OK).body_("OK").header_("Content-Type", "text/plain")),
            route("/echo")
            .bind(POST)
            .to(lambda req: Response(OK).body_(req.body.text).header_("Content-Type", "text/plain")),
            route("/hello/{name}").bind(GET).to(lambda req: Response(OK).body_("Hello, Anonymous!")),
        )

        # Wrap router with fallback for 404s
        def app_handler(request: Request) -> Response:
            response = router(request)
            return response if response else Response(NOT_FOUND).body_("Not Found")

        return StdLib(port=8080).to_server(app_handler)

    # Choose which server to run
    print("Starting simple server on http://localhost:8080")
    print("Try these endpoints:")
    print("  GET  /           - Welcome message")
    print("  GET  /health     - Health check")
    print("  POST /echo       - Echo request body")
    print("  GET  /hello/Alice - Personalized greeting")
    print("  Press Ctrl+C to stop")

    try:
        # Start the multi-route server
        server = multi_route_server()
        server.start().block()
    except KeyboardInterrupt:
        print("\nServer stopped")


if __name__ == "__main__":
    main()
