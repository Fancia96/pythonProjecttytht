import jwt
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser
)
from starlette.requests import Request
from starlette.responses import JSONResponse

import config
from users.users_service import UserService
from expections import expections
from expections.expections import Expection

db = config.db

secretto = config.secretto

users_service = UserService()


class APIAuthentication(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'jwt':
                return
            decoded = jwt.decode(credentials, secretto, algorithms=["HS256"])

            user_id = decoded['id']

            found_user = users_service.find_user_by_id(db, user_id)

            if found_user is None:
                raise Expection(expections.USER_EXIST, "Uzytkownik nie znaleziony")

            #searcherino, change password expection aaaan thatsit :duuno:




        except Expection as exccc:
            print(exccc)
            raise AuthenticationError('Invalid basic auth credentials')

        #username, _, password = decoded.partition(":")
        ###### : You'd want to verify the username and password here.
        return AuthCredentials(["authenticated"]), found_user

def on_auth_error(request: Request, exc: Exception):
    return JSONResponse({}, status_code=403)