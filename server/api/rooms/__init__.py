from starlette.routing import Route

from server.api.rooms.endpoints import MyRooms, CreateRoom, JoinRoom, GetRoom

routes = [
    Route("/my", MyRooms),
    Route("/create", CreateRoom),
    Route("/{id:int}/join", JoinRoom),
    Route("/{id:int}", GetRoom)
]
