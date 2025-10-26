from http4py.core import Request, Response
from http4py.core.method import POST
from http4py.core.status import OK

# Your app is just a function!
def echo(request: Request) -> Response:
    return Response(OK).body_(request.body)

response = echo(Request(POST, "/").body_("Hello!"))
print(response.body.text)  # "Hello!"
