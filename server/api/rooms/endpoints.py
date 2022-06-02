from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

import commands.roomsCommands
import config


db = config.db

class MyRooms(HTTPEndpoint):
    @requires('authenticated')
    async def get(self, request):

        try:

            user = request.user

            rooms_list = commands.roomsCommands.get_my_rooms_and_room_i_joined(db, user)

            print(rooms_list)

            rooms_list_json = []

            for room in rooms_list:
                print(user.get_name())
                json_users = {'name': room.get_unique_id(), 'id': room.get_id(), 'owner': room.get_owner_id()}
                rooms_list_json.append(json_users)


            print(rooms_list_json)

            return JSONResponse(rooms_list_json)

        except Exception as excc:
            return JSONResponse({'error': excc}, HTTP_400_BAD_REQUEST)


class CreateRoom(HTTPEndpoint):
    @requires('authenticated')
    async def post(self, request):

        try:
            jsonData = await request.json()

            user = request.user

            name = jsonData['name']
            password = jsonData['password']

            commands.roomsCommands.create_room(db, user, name, password)

            return JSONResponse({}, HTTP_200_OK)

        except Exception as excc:
            return JSONResponse({'error': excc}, HTTP_400_BAD_REQUEST)


class JoinRoom(HTTPEndpoint):
    @requires('authenticated')
    async def post(self, request):

        try:
            room_id = request.path_params['id']

            user = request.user

            commands.roomsCommands.join_room(db, room_id, user.get_id())

            return JSONResponse({}, HTTP_200_OK)

        except Exception as excc:
            return JSONResponse({'error': excc}, HTTP_400_BAD_REQUEST)


class GetRoom(HTTPEndpoint):
    @requires('authenticated')
    async def get(self, request):
        try:
            room_id = request.path_params['id']

            user = request.user

            rooms_list = commands.roomsCommands.get_a_room(db, user, room_id)

            print(rooms_list)

            rooms_list_json = []

            for room in rooms_list:
                print(user.get_name())
                json_users = {'name': room.get_unique_id(), 'id': room.get_id(), 'topic': room.get_owner_id(), 'users': [{'username':'hhhhh', 'username':'fffff'}], }
                rooms_list_json.append(json_users)

            return JSONResponse({}, HTTP_200_OK)

        except Exception as excc:
            return JSONResponse({'error': excc}, HTTP_400_BAD_REQUEST)

        # {“name”: “myName”, “id”: 8, “topic”: “my
        # topic”, “users”: [{
        # “username”: “test”
        # }, {
        # “username”: “test2”
        # }]}
        # Tylko
        # użytkownik
        # który
        # dołączył
        # do
        # pokoju

