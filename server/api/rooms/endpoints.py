import bcrypt
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, \
    HTTP_201_CREATED, HTTP_409_CONFLICT

import commands.roomsCommands
import config
import expections
from expections.expections import Expection

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

            return JSONResponse({}, HTTP_201_CREATED)

        except Expection as exp:
            if exp.code == expections.expections.ROOM_EXIST:
                return JSONResponse({'error': 'existing_room'}, HTTP_409_CONFLICT)
            else:
                return JSONResponse({'error': 'wrong_data'}, HTTP_400_BAD_REQUEST)


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


# class GetRoom(HTTPEndpoint):
#     @requires('authenticated')
#     async def get(self, request):
#         try:
#             room_id = request.path_params['id']
#
#             user = request.user
#
#             rooms_list = commands.roomsCommands.get_a_room(db, user, room_id)
#
#             print(rooms_list)
#
#             rooms_list_json = []
#
#             for room in rooms_list:
#                 print(user.get_name())
#                 json_users = {'name': room.get_unique_id(), 'id': room.get_id(), 'topic': room.get_owner_id(), 'users': [{'username':'hhhhh', 'username':'fffff'}], }
#                 rooms_list_json.append(json_users)
#
#             return JSONResponse({}, HTTP_200_OK)
#
#         except Exception as excc:
#             return JSONResponse({'error': excc}, HTTP_400_BAD_REQUEST)
#
#         # {“name”: “myName”, “id”: 8, “topic”: “my
#         # topic”, “users”: [{
#         # “username”: “test”
#         # }, {
#         # “username”: “test2”
#         # }]}
#         # Tylko
#         # użytkownik
#         # który
#         # dołączył
#         # do
#         # pokoju

class VoteSubject(HTTPEndpoint):
    @requires('authenticated')
    async def get(self, request):
        try:
            room_id = request.path_params['id']

            user = request.user

            room_votes_list = commands.roomsCommands.get_room_votes(db, room_id)

            # {
            # “votes”: [{
            # “username”: “test1”,
            # “value”: 1
            # }]
            # }

            print(room_votes_list)

            # room_users_list_json = []
            #
            # for room_vote in room_votes_list:
            #     # print(user.get_name())
            #     json_users = {'username': room_vote.get, 'value': }
            #     room_users_list_json.append(json_users)

            json_users = {'votes': list(room_votes_list)}

            return JSONResponse(json_users, HTTP_200_OK)

        except Exception as excc:
            return JSONResponse({'error': excc}, HTTP_400_BAD_REQUEST)

    @requires('authenticated')
    async def put(self, request):
        try:
            room_id = request.path_params['id']

            jsonData = await request.json()

            user = request.user

            vote = jsonData['vote']

            #{“vote”: 0.5}

            commands.roomsCommands.vote_a_room(db, room_id, user.get_id(), vote)

            return JSONResponse({}, HTTP_200_OK)

        except Exception as excc:
            return JSONResponse({'error': excc}, HTTP_400_BAD_REQUEST)

class Room(HTTPEndpoint):
    @requires('authenticated')
    async def get(self, request):
        try:
            room_id = request.path_params['id']
            room = commands.roomsCommands.get_a_room_by_id(db, room_id)

            if room is None:
                return JSONResponse({}, HTTP_404_NOT_FOUND)

            room_users = commands.roomsCommands.get_users_for_room(db, room_id)

            room_users_list_json = []

            for room_user in room_users:
                #print(user.get_name())
                json_users = {'username': room_user.get_name()}
                room_users_list_json.append(json_users)


            json_users = {'name': room.get_unique_id(), 'id': room.get_id(),
                          'topic': room.get_subject(),
                          'users': room_users_list_json}

            return JSONResponse(json_users, HTTP_200_OK)

        except Exception as excc:
            return JSONResponse({'error': excc}, HTTP_400_BAD_REQUEST)

    @requires('authenticated')
    async def patch(self, request):
        try:
            room_id = request.path_params['id']

            room = commands.roomsCommands.get_a_room_by_id(db, room_id)

            user = request.user

            print(room)
            if room is None:
                return JSONResponse({}, HTTP_404_NOT_FOUND)

            if user.get_id() != room.get_owner_id():
                return JSONResponse({}, HTTP_403_FORBIDDEN
                                    )
            # {“topic”: “new
            # topic”, “password”: “new
            # password”}
            #
            # {}
            #
            # {“topic”: “new
            # topic”}
            #
            # {“password”: “new”}


            jsonData = await request.json()

            if "topic" in jsonData:
                room.set_subject(jsonData['topic'])
                #print("ttututututututtut")


            if "password" in jsonData:
                room.set_password(bcrypt.hashpw(str(jsonData['password']).encode(), bcrypt.gensalt()).decode())

            user = request.user

            commands.roomsCommands.update_room(db, room)

            room_users = commands.roomsCommands.get_users_for_room(db, room_id)

            room_users_list_json = []

            for room_user in room_users:
                # print(user.get_name())
                json_users = {'username': room_user.get_name()}
                room_users_list_json.append(json_users)

            json_users = {'name': room.get_unique_id(), 'id': room.get_id(),
                          'topic': room.get_subject(),
                          'users': room_users_list_json}

            return JSONResponse(json_users, HTTP_200_OK)

        except Exception as excc:
            return JSONResponse({'error': excc}, HTTP_400_BAD_REQUEST)


