from enum import Enum


class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


GET = Method.GET
POST = Method.POST
PUT = Method.PUT
DELETE = Method.DELETE
PATCH = Method.PATCH
HEAD = Method.HEAD
OPTIONS = Method.OPTIONS
