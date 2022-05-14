# login register delete list users
import os

import bcrypt
from pip._internal import self_outdated_check

import database.database
from database.user_model import User
from database.room_model import Room

class RoomsService:

    def create_room(self, database, user: User, unique_id: str, password: str):
        # TODO hash the password
        room = Room(user.get_id(), unique_id, bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
        database.create_room(room, user)

        room = database.find_db_room(unique_id)
        return room

    def set_subject(self, database, room_id, subject: str):
        # TODO hash the password
        database.set_subject_db(room_id, subject)

        is_subject = database.is_subject_db(room_id)
        if is_subject:
            return True
        else:
            return False

    def add_points(self, database, room_id, points):
        # TODO hash the password

        database.add_points_db(room_id, points)

        return database.find_db_room_by_id(room_id).get_points()

    def are_you_room_owner(self, user_iq, room_owner_id):
        if user_iq == room_owner_id:
            return True
        return False

    def check_if_already_joined_this_room(self, database, room_id, user_id):
        return database.check_if_already_joined_this_room_db(room_id, user_id)

    def is_subject(self, database, room_id):
        return database.is_subject_db(room_id)


#first checked if you are owner
    def delete_room(self, database, room: Room, user: User):

        if self.are_you_room_owner(user.get_id(), room.get_owner_id()):
            database.delete_room_db(room, user)
            room = database.find_db_room(room.get_unique_id())
            return room
        else:
            print("Nie jesteś wlascicielem pokoju")
            return room



    def leave_room(self, database, user_id, room_id):
        database.leave_room_db(user_id, room_id)

        left_room = database.check_if_already_joined_this_room_db(room_id, user_id)
        return left_room

    def join_room(self, database, room_id, user_id):
        database.join_room_user(room_id, user_id)

        joined_room = database.check_if_already_joined_this_room_db(room_id, user_id)
        return joined_room

    def check_room_name(self, database, room_name, check_if_exists):
        alpha_numeric = "abcdefghijklmnopqrstuvwxyz0123456789"

        if len(room_name) == 0:
            print("Nazwa pokoju nie może być pusta")
            return False
        elif not all(c in alpha_numeric for c in room_name.lower()):
            print("Nazwa pokoju musi składać się z liter a-z oraz numerow 0-9 oraz nie zawierac spacji")
            return False
        elif check_if_exists and database.find_db_room(room_name):
            print("Podana nazwa pokoju już istnieje")
            return False

        return True

    def find_room(self, database, name, password, check_password):
        room = database.find_db_room(name)

        if check_password:
            if room and bcrypt.checkpw(password.encode(), room.get_password()):
                return room
            else:
                return None
        else:
            return room