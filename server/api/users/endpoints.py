import datetime

from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_200_OK

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
                return JSONResponse({'error': 'existing_user'}, HTTP_400_BAD_REQUEST)
            else:
                return JSONResponse({'error': 'wrong_data'}, HTTP_400_BAD_REQUEST)
        except:
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
    return jwt.encode({'id': user.get_id(), 'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=15)}, secretto, algorithm="HS256")

