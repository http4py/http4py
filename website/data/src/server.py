from http4py.server_uvicorn import Uvicorn

# Swap in any supported server runtime
server = Uvicorn(8080)

# Same function, now served on port 8080!
server.serve(echo).start().block()
