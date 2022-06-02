from database.user_model import User
from rooms.rooms_service import RoomsService

rooms_service = RoomsService()


def get_my_rooms_and_room_i_joined(db, user: User):
    rooms_list = rooms_service.get_my_rooms_and_room_i_joined(db, user)

    return rooms_list

def create_room(db, user: User, room_name, password):
    rooms_service.create_room(db, user, room_name, password)

def join_room(db, room_id, user_id):
    rooms_service.join_room(db, room_id, user_id)

def get_a_room(db, room_id, user_id):
    rooms_service.find_room_sub_an_vote(db, room_id, user_id)
