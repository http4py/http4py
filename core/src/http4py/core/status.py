from dataclasses import dataclass


@dataclass(frozen=True)
class Status:
    code: int
    description: str

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Status):
            return self.code == other.code
        return False

    def __hash__(self) -> int:
        return hash(self.code)


OK = Status(200, "OK")
CREATED = Status(201, "Created")
ACCEPTED = Status(202, "Accepted")
NO_CONTENT = Status(204, "No Content")

MOVED_PERMANENTLY = Status(301, "Moved Permanently")
FOUND = Status(302, "Found")
NOT_MODIFIED = Status(304, "Not Modified")

BAD_REQUEST = Status(400, "Bad Request")
UNAUTHORIZED = Status(401, "Unauthorized")
FORBIDDEN = Status(403, "Forbidden")
NOT_FOUND = Status(404, "Not Found")
METHOD_NOT_ALLOWED = Status(405, "Method Not Allowed")
CONFLICT = Status(409, "Conflict")

INTERNAL_SERVER_ERROR = Status(500, "Internal Server Error")
NOT_IMPLEMENTED = Status(501, "Not Implemented")
BAD_GATEWAY = Status(502, "Bad Gateway")
SERVICE_UNAVAILABLE = Status(503, "Service Unavailable")
