from starlette.routing import Mount

from server.api.users.__init__ import routes as users_routes
from server.api.rooms.__init__ import routes as rooms_routes

routes = [
    Mount("/users", routes=users_routes),
    Mount("/rooms", routes=rooms_routes)
]
