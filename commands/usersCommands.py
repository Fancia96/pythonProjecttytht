from users.users_service import UserService

users_service = UserService()


def login(db, login, password):
    return users_service.login(db, login, password)

def register(db, login, password):

    users_service.check_name(db, login)
        #print("Haslo co najmniej 8 znaków, duże i małe litery, cyfry i znaki specjalne")
    users_service.check_password(password)

    return users_service.register(db, login, password)
            #obj['user'] = user
            #click.echo("Zarejestrowano użytkownika")

