from expections import expections
from users.users_service import UserService
from expections.expections import Expection

users_service = UserService()


def login(db, login, password):
    user = users_service.login(db, login, password)
    # user = user_service.login(db, login, password)
    if user is None:
        raise Expection(expections.INVALID_USER_DATA, "Nieprawidłowy login lub hasło")
    else:
        print("Zalogowano")

    return

def find_all_users(db, str):
    users_list = db.find_db_all_users(str)

    return users_list

def register(db, login, password):

    users_service.check_name(db, login)
        #print("Haslo co najmniej 8 znaków, duże i małe litery, cyfry i znaki specjalne")
    users_service.check_password(password)

    return users_service.register(db, login, password)
            #obj['user'] = user
            #click.echo("Zarejestrowano użytkownika")

