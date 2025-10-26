#!/usr/bin/env python3

from http4py.core import Request, Response
from http4py.core.method import GET, POST
from http4py.core.status import OK, NOT_FOUND
from http4py.routing import routes, route
from http4py.server import Http4pyServer, StdLib


def main() -> None:
    def hello_world() -> Http4pyServer:
        def handler(req: Request) -> Response:
            return Response(OK).body_("Hello, World!")

        return StdLib(port=8080).serve(handler)

    def multi_route_server() -> Http4pyServer:
        app = routes(
            route("/").bind(GET).to(lambda req: Response(OK).body_("Welcome to http4py!")),
            route("/health").bind(GET).to(lambda req: Response(OK).body_("OK")),
            route("/echo").bind(POST).to(lambda req: Response(OK).body_(req.body)),
            route("/hello/{name}").bind(GET).to(lambda req: Response(OK).body_("Hello, Anonymous!")),
        )

        def app_handler(request: Request) -> Response:
            response = app(request)
            return response if response else Response(NOT_FOUND).body_("Not Found")

        return StdLib(port=8080).serve(app_handler)

    print("Starting simple server on http://localhost:8080")
    print("Try these endpoints:")
    print("  GET  /           - Welcome message")
    print("  GET  /health     - Health check")
    print("  POST /echo       - Echo request body")
    print("  GET  /hello/Alice - Personalized greeting")
    print("  Press Ctrl+C to stop")

    try:
        server = multi_route_server()
        server.start().block()
    except KeyboardInterrupt:
        print("\nServer stopped")


if __name__ == "__main__":
    main()
