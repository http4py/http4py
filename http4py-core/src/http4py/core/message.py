from __future__ import annotations

import dataclasses
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, BinaryIO

from .body import Body, _MemoryBody, _StreamBody
from .http_version import HttpVersion
from .method import Method
from .status import Status
from .uri import Uri


@dataclass(frozen=True, init=False)
class HttpMessage(ABC):
    headers: list[tuple[str, str | None]]
    body: Body
    version: HttpVersion

    #
    # def _init_http_message(self, version: HttpVersion = HttpVersion.HTTP_1_1) -> None:
    #     object.__setattr__(self, "headers", [])
    #     object.__setattr__(self, "body", _MemoryBody(""))
    #     object.__setattr__(self, "version", version)

    def header(self, name: str) -> str | None:
        for header_name, header_value in self.headers:
            if header_name.lower() == name.lower():
                return header_value
        return None

    def body_string(self) -> str:
        return self.body.text

    def close(self) -> None:
        self.body.close()

    @abstractmethod
    def body_(self, content: str | bytes | Body | BinaryIO) -> HttpMessage:
        pass

    @abstractmethod
    def header_(self, name: str, value: str | None) -> HttpMessage:
        pass

    @abstractmethod
    def headers_(self, headers: list[tuple[str, str | None]]) -> HttpMessage:
        pass


@dataclass(frozen=True)
class Request(HttpMessage):
    method: Method
    uri: Uri

    @staticmethod
    def of(method: Method, uri: str | Uri, version: HttpVersion = HttpVersion.HTTP_1_1) -> Request:
        return Request(
            headers=[],
            body=_MemoryBody(""),
            version=version,
            method=method,
            uri=uri if isinstance(uri, Uri) else Uri.of(uri)
        )

    def body_(self, content: str | bytes | Body | BinaryIO) -> Request:
        if isinstance(content, Body):
            new_body = content
        elif isinstance(content, (str, bytes)):
            new_body = _MemoryBody(content)
        else:
            new_body = _StreamBody(content)

        return dataclasses.replace(self, body=new_body)

    def header_(self, name: str, value: str | None) -> Request:
        return dataclasses.replace(self, headers=self.headers + [(name, value)])

    def headers_(self, headers: list[tuple[str, str | None]]) -> Request:
        return dataclasses.replace(self, headers=self.headers + headers)


@dataclass(frozen=True)
class Response(HttpMessage):
    status: Status

    @staticmethod
    def of(status: Status, version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response(
            headers=[],
            body=_MemoryBody(""),
            version=version,
            status=status
        )

    def body_(self, content: str | bytes | Body | BinaryIO) -> Response:
        if isinstance(content, Body):
            new_body = content
        elif isinstance(content, (str, bytes)):
            new_body = _MemoryBody(content)
        else:
            new_body = _StreamBody(content)

        return dataclasses.replace(self, body=new_body)

    def header_(self, name: str, value: str | None) -> Response:
        return dataclasses.replace(self, headers=self.headers + [(name, value)])

    def headers_(self, headers: list[tuple[str, str | None]]) -> Response:
        return dataclasses.replace(self, headers=self.headers + headers)
