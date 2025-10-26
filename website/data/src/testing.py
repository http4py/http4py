from http4py.core import Request
from http4py.core.method import POST
from http4py.core.status import OK

# Test your app without spinning up servers!
def test_echo_handler():
    request = Request(POST, "/").body_("test")
    response = echo(request)  # Just call your function!

    assert response.status == OK
    assert response.body.text == "test"
