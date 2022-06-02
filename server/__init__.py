from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.routing import Mount

from server.api.__init__ import routes as api_routes
from server.api.middleware import APIAuthentication, on_auth_error

routes = [
    Mount("/api", routes=api_routes, name="api"),
]


middleware = [Middleware(AuthenticationMiddleware, backend=APIAuthentication(), on_error=on_auth_error),
              Middleware(TrustedHostMiddleware, allowed_hosts=['*']),
              Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
              ]

app = Starlette(routes=routes, middleware=middleware, debug=True)
