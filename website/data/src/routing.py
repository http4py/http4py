from http4py.core import Request, Response
from http4py.core.method import GET, POST
from http4py.core.status import OK
from http4py.routing import routes, route

# Add routing to combine multiple handlers
app = routes(
    route("/echo").bind(POST).to(echo),
    route("/").bind(GET).to(
        lambda req: Response(OK).body_("Welcome!")
    )
)

response = app(Request(POST, "/echo").body_("Hello!"))
