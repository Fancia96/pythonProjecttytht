# login register delete list users
import os

import bcrypt
from pip._internal import self_outdated_check

import database.database
import expections
from database.user_model import User
from database.room_model import Room
from expections.expections import Expection

class RoomsService:

    def create_room(self, database, user: User, unique_id: str, password: str):
        # TODO hash the password
        room = Room(owner_id=user.id, owner=user, name=unique_id,
                    password=str(bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()))
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

    def are_you_room_owner(self, user_iq, room_owner_id):
        if user_iq == room_owner_id:
            return True
        return False

    def check_if_already_joined_this_room(self, database, room_id, user: User):
        return database.check_if_already_joined_this_room_db(room_id, user)

    def is_subject(self, database, room_id):
        return database.is_subject_db(room_id)


#first checked if you are owner
    def delete_room(self, database, room: Room, user: User):

        if self.are_you_room_owner(user.id, room.owner_id):
            database.delete_room_db(room, user)
            room = database.find_db_room(room.name)
            return room
        else:
            print("Nie jesteś wlascicielem pokoju")
            return room



    def leave_room(self, database, user: User, room: Room):
        database.leave_room_db(user, room)

        left_room = database.check_if_already_joined_this_room_db(room.id, user)
        return left_room

    def join_room(self, database, room_id, user: User):

        #joined_room = database.check_if_already_joined_this_room_db(room_id, user_id)
        return database.join_room_user(room_id, user)

    def check_room_name(self, database, room_name, check_if_exists):
        # alpha_numeric = "abcdefghijklmnopqrstuvwxyz0123456789"
        #
        # if len(room_name) == 0:
        #     print("Nazwa pokoju nie może być pusta")
        #     return False
        # elif not all(c in alpha_numeric for c in room_name.lower()):
        #     print("Nazwa pokoju musi składać się z liter a-z oraz numerow 0-9 oraz nie zawierac spacji")
        #     return False
        # elif check_if_exists and database.find_db_room(room_name):
        #     print("Podana nazwa pokoju już istnieje")
        #     return False
        #
        # return True
        alpha_numeric = "abcdefghijklmnopqrstuvwxyz0123456789"

        if len(room_name) == 0:
            # print("Nazwa nie może być pusta")
            raise Expection(expections.expections.INVALID_ROOM_DATA, "Nazwa pokoju nie może być pusta")
            # return False
        elif not all(c in alpha_numeric for c in room_name.lower()):
            # print("Nazwa musi składać się z liter a-z oraz numerow 0-9 oraz nie zawierac spacji")
            raise Expection(expections.expections.INVALID_ROOM_DATA,
                            "Nazwa pokoju musi składać się z liter a-z oraz numerow 0-9 oraz nie zawierac spacji")
            # return False
        elif check_if_exists and database.find_db_room(room_name):
            # print("Podana nazwa użytkownika już istnieje")
            raise Expection(expections.expections.ROOM_EXIST, "Podana nazwa pokoju już istnieje")
            # return False

        return True


    def find_room(self, database, name, password, check_password):
        room = database.find_db_room(name)

        if check_password:
            if room and bcrypt.checkpw(password.encode(), room.password.encode()):
                return room
            else:
                return None
        else:
            return room

    def find_room_sub_an_vote(self, database, name, password, check_password):
        room = database.find_db_room(name)

        if check_password:
            if room and bcrypt.checkpw(password.encode(), room.get_password()):
                return room
            else:
                return None
        else:
            return room

    def get_users_for_room(self, database, room_id):
        room = database.find_db_room_users(room_id)

        return room

    def get_a_room_users_db(self, database, name):
        room = database.find_db_room(name)

        return room

    def get_a_room_by_id_db(self, database, room_id):
        room = database.find_db_room_by_id(room_id)

        return room

    def update_room(self, database, room: Room, subjectChanged):
        room = database.update_room_db(room, subjectChanged)

        return room

    def get_my_rooms_and_room_i_joined(self, database, user: User):
        rooms_list = database.get_my_rooms_and_room_i_joined(user)

        return rooms_list

    def get_room_votes(self, database, room_id):
        room = database.get_room_votes(room_id)

        return room

    def set_room_votes(self, database, room: Room, user: User, points):
        room = database.add_points_db(room, user, points)

        return room
