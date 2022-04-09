# login register delete list users
import os

import database.database
from database.user_model import User
from database.room_model import Room

class RoomsService:

    def create_room(self, user: User, unique_id: str, password: str):
        # TODO hash the password
        room = Room(unique_id, password)
        database.database.create_room(room, user)

        room = database.database.find_db_room(unique_id)
        return room

#first checked if you are owner
    def delete_room(self, room: Room, user: User):
        database.database.delete_room(room, user)
        room = database.database.find_db_room(room.get_unique_id())
        return room

    def leave_room(self, room_name, user: User):
        database.database.leave_room(room_name, user)

        left_room = database.database.check_if_already_joined_this_room(room_name, user)
        return left_room

    def join_room(self, room_name, user: User):
        database.database.join_room_user(room_name, user)

        joined_room = database.database.check_if_already_joined_this_room(room_name, user)
        return joined_room

    def check_room_name(self, room_name, check_if_exists):
        alpha_numeric = "abcdefghijklmnopqrstuvwxyz0123456789"

        if len(room_name) == 0:
            print("Nazwa pokoju nie może być pusta")
            return False
        elif not all(c in alpha_numeric for c in room_name.lower()):
            print("Nazwa pokoju musi składać się z liter a-z oraz numerow 0-9 oraz nie zawierac spacji")
            return False
        elif check_if_exists and database.database.find_db_room(room_name):
            print("Podana nazwa pokoju już istnieje")
            return False

        return True