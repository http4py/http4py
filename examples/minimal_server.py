#!/usr/bin/env python3
"""
Minimal HTTP Server Example

The absolute simplest http4py server - just one line!
"""

from http4py.core import Response
from http4py.core.status import OK
from http4py.server import StdLib

if __name__ == "__main__":
    print("Starting minimal server on http://localhost:8080")
    print("Visit http://localhost:8080 to see 'Hello, http4py!'")
    print("Press Ctrl+C to stop")

    StdLib(8080).to_server(lambda req: Response(OK).body_("Hello, http4py!")).start().block()
