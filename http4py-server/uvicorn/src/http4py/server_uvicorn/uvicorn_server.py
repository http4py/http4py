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

                self._thread = threading.Thread(target=self._server.run, daemon=True)
                self._thread.start()

                asyncio.run(self.wait_for_started())

                return self

            def stop(self) -> Http4pyServer:
                if self._thread.is_alive():
                    self._server.should_exit = True
                    while self._thread.is_alive():
                        continue

                return self

            def block(self) -> None:
                if self._thread is not None:
                    self._thread.join()

            def port(self) -> int:
                return self._port

            async def wait_for_started(self):
                while not self._server.started:
                    await asyncio.sleep(0.1)

                if self._server.config.port == 0:
                    for server in self._server.servers:
                        self._port = server.sockets[0].getsockname()[1]

        return _UvicornServer(self._port, http)
