from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.routing import Mount

from server.api.__init__ import routes as api_routes
from server.api.middleware import APIAuthentication, on_auth_error

routes = [
    Mount("/api", routes=api_routes, name="api"),
]

middleware = [Middleware(AuthenticationMiddleware, backend=APIAuthentication(), on_error=on_auth_error)]

app = Starlette(routes=routes, middleware=middleware, debug=True)
