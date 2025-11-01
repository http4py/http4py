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
    def get(uri: str | Uri, version: HttpVersion = HttpVersion.HTTP_1_1) -> Request:
        return Request.for_method(Method.GET, uri, version)

    @staticmethod
    def post(uri: str | Uri, version: HttpVersion = HttpVersion.HTTP_1_1) -> Request:
        return Request.for_method(Method.POST, uri, version)

    @staticmethod
    def put(uri: str | Uri, version: HttpVersion = HttpVersion.HTTP_1_1) -> Request:
        return Request.for_method(Method.PUT, uri, version)

    @staticmethod
    def delete(uri: str | Uri, version: HttpVersion = HttpVersion.HTTP_1_1) -> Request:
        return Request.for_method(Method.DELETE, uri, version)

    @staticmethod
    def patch(uri: str | Uri, version: HttpVersion = HttpVersion.HTTP_1_1) -> Request:
        return Request.for_method(Method.PATCH, uri, version)

    @staticmethod
    def head(uri: str | Uri, version: HttpVersion = HttpVersion.HTTP_1_1) -> Request:
        return Request.for_method(Method.HEAD, uri, version)

    @staticmethod
    def options(uri: str | Uri, version: HttpVersion = HttpVersion.HTTP_1_1) -> Request:
        return Request.for_method(Method.OPTIONS, uri, version)

    @staticmethod
    def for_method(method: Method, uri: str | Uri, version: HttpVersion = HttpVersion.HTTP_1_1) -> Request:
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

    # def __init__(self, status: Status, version: HttpVersion = HttpVersion.HTTP_1_1):
    #     self._init_http_message(version)
    #     object.__setattr__(self, "status", status)

    # def _copy(self, **overrides: Any) -> Response:
    #     new_response = Response(overrides.get("status", self.status), overrides.get("version", self.version))
    #     object.__setattr__(new_response, "headers", list(overrides.get("headers", self.headers)))
    #     object.__setattr__(new_response, "body", overrides.get("body", self.body))
    #     return new_response
    @staticmethod
    def ok(version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response.for_status(Status.OK, version)

    @staticmethod
    def created(version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response.for_status(Status.CREATED, version)

    @staticmethod
    def accepted(version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response.for_status(Status.ACCEPTED, version)

    @staticmethod
    def no_content(version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response.for_status(Status.NO_CONTENT, version)

    @staticmethod
    def moved_permanently(version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response.for_status(Status.MOVED_PERMANENTLY, version)

    @staticmethod
    def found(version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response.for_status(Status.FOUND, version)

    @staticmethod
    def not_modified(version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response.for_status(Status.NOT_MODIFIED, version)

    @staticmethod
    def bad_request(version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response.for_status(Status.BAD_REQUEST, version)

    @staticmethod
    def unauthorized(version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response.for_status(Status.UNAUTHORIZED, version)

    @staticmethod
    def forbidden(version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response.for_status(Status.FORBIDDEN, version)

    @staticmethod
    def not_found(version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response.for_status(Status.NOT_FOUND, version)

    @staticmethod
    def method_not_allowed(version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response.for_status(Status.METHOD_NOT_ALLOWED, version)

    @staticmethod
    def conflict(version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response.for_status(Status.CONFLICT, version)

    @staticmethod
    def internal_server_error(version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response.for_status(Status.INTERNAL_SERVER_ERROR, version)

    @staticmethod
    def not_implemented(version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response.for_status(Status.NOT_IMPLEMENTED, version)

    @staticmethod
    def bad_gateway(version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response.for_status(Status.BAD_GATEWAY, version)

    @staticmethod
    def service_unavailable(version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
        return Response.for_status(Status.SERVICE_UNAVAILABLE, version)

    @staticmethod
    def for_status(status: Status, version: HttpVersion = HttpVersion.HTTP_1_1) -> Response:
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
