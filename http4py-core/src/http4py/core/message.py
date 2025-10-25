from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, BinaryIO

from .body import Body, _MemoryBody, _StreamBody
from .http_version import HttpVersion
from .method import Method
from .status import Status
from .uri import Uri


@dataclass(frozen=True, init=False)
class HttpMessage(ABC):
    headers: dict[str, str]
    body: Body
    version: HttpVersion

    def _init_http_message(self, version: HttpVersion = HttpVersion.HTTP_1_1) -> None:
        object.__setattr__(self, "headers", {})
        object.__setattr__(self, "body", _MemoryBody(""))
        object.__setattr__(self, "version", version)

    def header(self, name: str) -> str | None:
        return self.headers.get(name)

    def body_string(self) -> str:
        return self.body.text

    def close(self) -> None:
        self.body.close()

    @abstractmethod
    def body_(self, content: str | bytes | Body | BinaryIO) -> HttpMessage:
        pass

    @abstractmethod
    def header_(self, name: str, value: str) -> HttpMessage:
        pass

    @abstractmethod
    def headers_(self, headers: dict[str, str]) -> HttpMessage:
        pass


@dataclass(frozen=True, init=False)
class Request(HttpMessage):
    method: Method
    uri: Uri

    def __init__(self, method: Method, uri: str | Uri, version: HttpVersion = HttpVersion.HTTP_1_1):
        self._init_http_message(version)
        object.__setattr__(self, "method", method)
        object.__setattr__(self, "uri", uri if isinstance(uri, Uri) else Uri.of(uri))

    def _copy(self, **overrides: Any) -> Request:
        new_request = Request(
            overrides.get("method", self.method), overrides.get("uri", self.uri), overrides.get("version", self.version)
        )
        object.__setattr__(new_request, "headers", overrides.get("headers", self.headers).copy())
        object.__setattr__(new_request, "body", overrides.get("body", self.body))
        return new_request

    def body_(self, content: str | bytes | Body | BinaryIO) -> Request:
        if isinstance(content, Body):
            new_body = content
        elif isinstance(content, (str, bytes)):
            new_body = _MemoryBody(content)
        else:
            new_body = _StreamBody(content)

        return self._copy(body=new_body)

    def header_(self, name: str, value: str) -> Request:
        new_headers = self.headers.copy()
        new_headers[name] = value
        return self._copy(headers=new_headers)

    def headers_(self, headers: dict[str, str]) -> Request:
        new_headers = self.headers.copy()
        new_headers.update(headers)
        return self._copy(headers=new_headers)


@dataclass(frozen=True, init=False)
class Response(HttpMessage):
    status: Status

    def __init__(self, status: Status, version: HttpVersion = HttpVersion.HTTP_1_1):
        self._init_http_message(version)
        object.__setattr__(self, "status", status)

    def _copy(self, **overrides: Any) -> Response:
        new_response = Response(overrides.get("status", self.status), overrides.get("version", self.version))
        object.__setattr__(new_response, "headers", overrides.get("headers", self.headers).copy())
        object.__setattr__(new_response, "body", overrides.get("body", self.body))
        return new_response

    def body_(self, content: str | bytes | Body | BinaryIO) -> Response:
        if isinstance(content, Body):
            new_body = content
        elif isinstance(content, (str, bytes)):
            new_body = _MemoryBody(content)
        else:
            new_body = _StreamBody(content)

        return self._copy(body=new_body)

    def header_(self, name: str, value: str) -> Response:
        new_headers = self.headers.copy()
        new_headers[name] = value
        return self._copy(headers=new_headers)

    def headers_(self, headers: dict[str, str]) -> Response:
        new_headers = self.headers.copy()
        new_headers.update(headers)
        return self._copy(headers=new_headers)
