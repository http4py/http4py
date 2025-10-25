from __future__ import annotations

from enum import Enum


class Status(Enum):
    OK = (200, "OK")
    CREATED = (201, "Created")
    ACCEPTED = (202, "Accepted")
    NO_CONTENT = (204, "No Content")

    MOVED_PERMANENTLY = (301, "Moved Permanently")
    FOUND = (302, "Found")
    NOT_MODIFIED = (304, "Not Modified")

    BAD_REQUEST = (400, "Bad Request")
    UNAUTHORIZED = (401, "Unauthorized")
    FORBIDDEN = (403, "Forbidden")
    NOT_FOUND = (404, "Not Found")
    METHOD_NOT_ALLOWED = (405, "Method Not Allowed")
    CONFLICT = (409, "Conflict")

    INTERNAL_SERVER_ERROR = (500, "Internal Server Error")
    NOT_IMPLEMENTED = (501, "Not Implemented")
    BAD_GATEWAY = (502, "Bad Gateway")
    SERVICE_UNAVAILABLE = (503, "Service Unavailable")

    def __init__(self, code: int, description: str):
        self.code = code
        self.description = description

    @classmethod
    def from_code(cls, code: int) -> Status:
        for status in cls:
            if status.code == code:
                return status
        raise ValueError(f"Unknown HTTP status code: {code}")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Status):
            return self.code == other.code
        return False

    def __hash__(self) -> int:
        return hash(self.code)


OK = Status.OK
CREATED = Status.CREATED
ACCEPTED = Status.ACCEPTED
NO_CONTENT = Status.NO_CONTENT
MOVED_PERMANENTLY = Status.MOVED_PERMANENTLY
FOUND = Status.FOUND
NOT_MODIFIED = Status.NOT_MODIFIED
BAD_REQUEST = Status.BAD_REQUEST
UNAUTHORIZED = Status.UNAUTHORIZED
FORBIDDEN = Status.FORBIDDEN
NOT_FOUND = Status.NOT_FOUND
METHOD_NOT_ALLOWED = Status.METHOD_NOT_ALLOWED
CONFLICT = Status.CONFLICT
INTERNAL_SERVER_ERROR = Status.INTERNAL_SERVER_ERROR
NOT_IMPLEMENTED = Status.NOT_IMPLEMENTED
BAD_GATEWAY = Status.BAD_GATEWAY
SERVICE_UNAVAILABLE = Status.SERVICE_UNAVAILABLE
