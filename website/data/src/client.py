from http4py.client import StdLibClient
from http4py.core import Request
from http4py.core.method import GET

# An HTTP client is just another HttpHandler function!
client = StdLibClient()

response = client(Request(GET, "https://httpbin.org/get"))

print(f"Status: {response.status}")  # 200 OK
print(f"Content-Type: {response.header('content-type')}")
