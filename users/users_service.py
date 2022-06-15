# login register delete list users
import os
import bcrypt
import database.database
import expections.expections

from database.user_model import User
from database.database import Database
from expections.expections import Expection


class UserService:

    #TODO tu powinien byc obiekt usera
    def login(self, database, name, password):
        user = database.find_db_user(name)

        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            return user
        else:
            return None

    def check_name(self, database, name):
        alpha_numeric = "abcdefghijklmnopqrstuvwxyz0123456789"

        if len(name) == 0:
            #print("Nazwa nie może być pusta")
            raise Expection(expections.expections.INVALID_USER_DATA, "Nazwa nie może być pusta")
            #return False
        elif not all(c in alpha_numeric for c in name.lower()):
            #print("Nazwa musi składać się z liter a-z oraz numerow 0-9 oraz nie zawierac spacji")
            raise Expection(expections.expections.INVALID_USER_DATA, "Nazwa musi składać się z liter a-z oraz numerow 0-9 oraz nie zawierac spacji")
            #return False
        elif database.find_db_user(name):
            #print("Podana nazwa użytkownika już istnieje")
            raise Expection(expections.expections.USER_EXIST, "Podana nazwa użytkownika już istnieje")
            #return False

        return True

    def check_password(self, password):
        bad_password_length = True
        bad_password_small_letter = True
        bad_password_big_letter = True
        bad_password_numbers = True
        bad_password_specials = True

        special_characters = "!@#$%^&*()-+?_=,.{}\<>/"

        error_massage = ""

        if len(password) < 8:
            error_massage += "haslo za krotkie \n"
            bad_password_length = False
        if not any(char.isdigit() for char in password):
            error_massage += "haslo musi zawierać cyfrę \n"
            bad_password_numbers = False
        if password.upper() == password:
            error_massage += "haslo musi zawierać małe litery \n"
            bad_password_small_letter = False
        if password.lower() == password:
            error_massage += "haslo musi zawierać duże litery \n"
            bad_password_big_letter = False
        if not any(c in special_characters for c in password):
            error_massage += "haslo musi zawierać znak specjalny \n"
            bad_password_specials = False
        if ' ' in password == True:
            error_massage += "haslo nie moze zawierac spacji \n"
            bad_password_specials = False

        if bad_password_length and bad_password_numbers and bad_password_small_letter and bad_password_big_letter and bad_password_specials:
            return True
        else:
            #return False
            raise Expection(expections.expections.INVALID_USER_DATA,
                        error_massage)

    def register(self, database, name, password):
        # TODO hash the password
        user = User(username=name)
        user.password = str(bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode())

        return database.write_db_user(user)

    def find_user_by_id(self, database, id):
        user = database.find_db_user_by_id(id)

        if user:
            return user
        else:
            return None

    def delete_user(self, database, user: User):

        name = user.username
        database.delete_db_user(user)

        #delete all rooms and users in

        # for room in database.database.get_my_rooms(user):
        #     database.delete_room(room, user)
        #
        # database.delete_my_room_connections(user)

        user = database.find_db_user(name)
        return user
