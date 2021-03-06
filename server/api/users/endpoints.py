import datetime

from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_409_CONFLICT

import commands.usersCommands
import config
import expections.expections
from database import database

import jwt

from database.user_model import User
from expections.expections import Expection

db = config.db

secretto = config.secretto

class Login(HTTPEndpoint):
    async def post(self, request):

        try:
            jsonData = await request.json()

            login = jsonData['login']
            password = jsonData['password']

            print(login)
            print(password)

            user: User = commands.usersCommands.login(db, login, password)
            if user:
                #TOKENO

                token = createToken(user)

                return JSONResponse({'token': token})
            else:
                return JSONResponse({}, HTTP_401_UNAUTHORIZED)

            #return PlainTextResponse(f"Hello, weeeorld! " + jsonData['login'])
        except Expection as exp:
            return JSONResponse({'error': exp.massage}, HTTP_400_BAD_REQUEST)
        except Exception as excc:
            return JSONResponse({'error': excc}, HTTP_400_BAD_REQUEST)




# class CreateRoom(HTTPEndpoint):
#     async def post(self, request):
#         #createroom()
#         pass

class Register(HTTPEndpoint):
    async def post(self, request):
        try:
            jsonData = await request.json()

            login = jsonData['login']
            password = jsonData['password']

            print(login)
            print(password)

            user: User = commands.usersCommands.register(db, login, password)

            return JSONResponse({}, HTTP_200_OK)

            # return PlainTextResponse(f"Hello, weeeorld! " + jsonData['login'])
        except Expection as exp:
            if exp.code == expections.expections.USER_EXIST:
                return JSONResponse({'error': 'existing_user'}, HTTP_409_CONFLICT)
            else:
                return JSONResponse({'error': 'wrong_data'}, HTTP_400_BAD_REQUEST)

class Refresh(HTTPEndpoint):
    @requires('authenticated')
    async def post(self, request):
       # token = request.headers['Authorization']

        user = request.user

        token = createToken(user)

        return JSONResponse({'token': token})
        #


def createToken(user: User):
    return jwt.encode({'id': user.id, 'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=15)}, secretto, algorithm="HS256")

class List(HTTPEndpoint):
    @requires('authenticated')
    async def get(self, request):

        try:
            query_param_filter = ""

            if "filter" in request.query_params:
                query_param_filter = request.query_params['filter']

            users_list = commands.usersCommands.find_all_users(db, query_param_filter)

            users_list_json = []

            for user in users_list:
                print(user.username)
                json_users = {'username': user.username}
                users_list_json.append(json_users)
            # create json

            print(users_list_json)

            return JSONResponse(users_list_json)

        except Exception as excc:
            return JSONResponse({'error': excc}, HTTP_400_BAD_REQUEST)
