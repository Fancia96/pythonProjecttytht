from starlette.routing import Route
from server.api.users.endpoints import Login, Register, Refresh, List

routes = [
    Route("/login", Login),
    Route("/register", Register),
    Route("/refresh", Refresh),

    Route("/list", List)
]
