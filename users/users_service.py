# login register delete list users
import os
import bcrypt
import database.database
from database.user_model import User
from database.database import Database


class UserService:

    #TODO tu powinien byc obiekt usera
    def login(self, database, name, password):
        user = database.find_db_user(name)

        if user and bcrypt.checkpw(password.encode(), user.get_password()):
            return user
        else:
            return None

    def check_name(self, database, name):
        alpha_numeric = "abcdefghijklmnopqrstuvwxyz0123456789"

        if len(name) == 0:
            print("Nazwa nie może być pusta")
            return False
        elif not all(c in alpha_numeric for c in name.lower()):
            print("Nazwa musi składać się z liter a-z oraz numerow 0-9 oraz nie zawierac spacji")
            return False
        elif database.find_db_user(name):
            print("Podana nazwa użytkownika już istnieje")
            return False

        return True

    def check_password(self, password):
        bad_password_length = True
        bad_password_small_letter = True
        bad_password_big_letter = True
        bad_password_numbers = True
        bad_password_specials = True

        special_characters = "!@#$%^&*()-+?_=,.{}\<>/"

        if len(password) < 8:
            print("haslo za krotkie")
            bad_password_length = False
        if not any(char.isdigit() for char in password):
            print("haslo musi zawierać cyfrę")
            bad_password_numbers = False
        if password.upper() == password:
            print("haslo musi zawierać małe litery")
            bad_password_small_letter = False
        if password.lower() == password:
            print("haslo musi zawierać duże litery")
            bad_password_big_letter = False
        if not any(c in special_characters for c in password):
            print("haslo musi zawierać znak specjalny")
            bad_password_specials = False
        if ' ' in password == True:
            print("haslo nie moze zawierac spacji")
            bad_password_specials = False

        if bad_password_length and bad_password_numbers and bad_password_small_letter and bad_password_big_letter and bad_password_specials:
            return True
        else:
            return False

    def register(self, database, name, password):
        # TODO hash the password
        user = User(name, bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
        user_id = database.write_db_user(user)
        user.set_id(user_id)

        return user

    def find_all_users(self, database, text):
        print("Znalezieni użytkownicy:")
        for user in database.find_db_all_users(text):
            print(user.get_name())

    def delete_user(self, database, user: User):
        database.delete_db_user(user)

        #delete all rooms and users in

        # for room in database.database.get_my_rooms(user):
        #     database.delete_room(room, user)
        #
        # database.delete_my_room_connections(user)

        user = database.find_db_user(user.get_name())
        return user
