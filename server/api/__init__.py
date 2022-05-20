from starlette.routing import Mount

from server.api.users.__init__ import routes as users_routes

routes = [
    Mount("/users", routes=users_routes)
]
