from __future__ import annotations

import asyncio
import threading

import uvicorn
from http4py.core import HttpHandler
from http4py.server import Http4pyServer, ServerConfig
from http4py.server_asgi import StandardAsgiAdapter


class Uvicorn(ServerConfig):
    def __init__(self, port: int = 8080):
        self._port = port

    def serve(self, http: HttpHandler) -> Http4pyServer:
        class _UvicornServer(Http4pyServer):
            def __init__(self, port: int, http_handler: HttpHandler):
                self._port = port
                self._http_handler = http_handler
                self._server: uvicorn.Server | None = None
                self._thread: threading.Thread | None = None
                self._loop: asyncio.AbstractEventLoop | None = None

            def start(self) -> Http4pyServer:
                if self._server is not None:
                    return self

                config = uvicorn.Config(
                    app=StandardAsgiAdapter().to_asgi(self._http_handler),
                    host="localhost",
                    port=self._port,
                    access_log=False,
                )
                self._server = uvicorn.Server(config)

                def run_server() -> None:
                    self._loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(self._loop)
                    if self._server is not None:
                        self._loop.run_until_complete(self._server.serve())

                self._thread = threading.Thread(target=run_server, daemon=True)
                self._thread.start()

                while self._server is None or not self._server.started:
                    pass

                return self

            def stop(self) -> Http4pyServer:
                if self._server is not None and self._loop is not None:
                    self._loop.call_soon_threadsafe(self._server.should_exit.__setattr__, "value", True)
                    if self._thread is not None:
                        self._thread.join()
                    self._server = None
                    self._thread = None
                    self._loop = None
                return self

            def block(self) -> None:
                if self._thread is not None:
                    self._thread.join()

            def port(self) -> int:
                return self._port

        return _UvicornServer(self._port, http)
