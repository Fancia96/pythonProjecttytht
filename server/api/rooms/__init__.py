from starlette.routing import Route

from server.api.rooms.endpoints import MyRooms, CreateRoom, JoinRoom, VoteSubject, Room

routes = [
    Route("/my", MyRooms),
    Route("/create", CreateRoom),
    Route("/{id:int}/join", JoinRoom),

    Route("/{id:int}", Room),

    Route("/{id:int}/vote", VoteSubject)
    #Route("/{id:int}/vote", VoteSubject)
]
