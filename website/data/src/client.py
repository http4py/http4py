from http4py.client import stdlib_client
from http4py.core import Request
from http4py.core.method import GET

# Client is just another HttpHandler function!
request = Request(GET, "https://httpbin.org/get")
response = stdlib_client(request)

print(f"Status: {response.status}")  # 200 OK
print(f"Content-Type: {response.header('content-type')}")
