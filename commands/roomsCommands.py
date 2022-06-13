from database.room_model import Room
from database.user_model import User
from rooms.rooms_service import RoomsService
from users.users_service import UserService

rooms_service = RoomsService()
users_service = UserService()


def get_my_rooms_and_room_i_joined(db, user: User):
    rooms_list = rooms_service.get_my_rooms_and_room_i_joined(db, user)

    return rooms_list

def create_room(db, user: User, room_name, password):
    rooms_service.check_room_name(db, room_name, True)
    # print("Haslo co najmniej 8 znaków, duże i małe litery, cyfry i znaki specjalne")
    users_service.check_password(password)

    rooms_service.create_room(db, user, room_name, password)

def join_room(db, room_id, user_id):
    rooms_service.join_room(db, room_id, user_id)

def get_a_room(db, room_id, user_id):
    rooms_service.find_room_sub_an_vote(db, room_id, user_id)

def get_a_room_by_id(db, room_id):
    return rooms_service.get_a_room_by_id_db(db, room_id)

def get_users_for_room(db, room_id):
    return rooms_service.get_users_for_room(db, room_id)

def update_room(db, room: Room):
    return rooms_service.update_room(db, room)

def get_room_votes(db, room_id):
    return rooms_service.get_room_votes(db, room_id)

def vote_a_room(db, room_id, user_id, vote):
    return rooms_service.set_room_votes(db, room_id, user_id, vote)


