from dataclasses import dataclass

from http4py.core import Filter, HttpHandler, Request, Response
from http4py.core.method import POST


# Filters are just middleware that decorate a handler
@dataclass(frozen=True)
class ReverseContent(Filter):
    def __call__(self, next: HttpHandler) -> HttpHandler:
        def decorated(request: Request) -> Response:
            reversed_body = request.body.text[::-1]
            return next(request.body_(reversed_body))

        return decorated

# combining filters/handlers is just composing functions
reversed_echo = ReverseContent().then(echo)
response = reversed_echo(Request(POST, "/").body_("Hello!"))
print(response.body.text)  # "!olleH"
