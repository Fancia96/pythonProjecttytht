import csv
import os
import sys

current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
#print(current_dir)
#print(os.path.join(current_dir, "../db_users.csv"))
db_users_path = os.path.join(current_dir, "db_users.csv")
db_rooms_path = os.path.join(current_dir, "db_rooms.csv")
db_rooms_users_path = os.path.join(current_dir, "db_rooms_users.csv")

#class DatabaseClass:

def check_db_exist(path):
    try:
        os.stat(path)
    except FileNotFoundError:
        f = open(path, "w")
        f.close()

def write_db_user(user, password):
    with open(db_path, 'a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([user.get_name(), user.get_password().decode()])

def find_db_user(user_name: str):
    with open(db_users_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
             if user_name.upper() == line[0].upper():
                return User(line[0], line[1].encode())
        return None

def find_db_all_users(filter_string):

    print("Znalezieni użytkownicy:")

    with open(db_users_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if filter_string and filter_string.upper() in line[0].upper():
                print(line[0])
            elif not filter_string:
                print(line[0])

def delete_db_user(user):

    array_of_users = []

    with open(db_users_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if not user.upper() == line[0].upper():
                array_of_users.append(line)

    with open(db_users_path, 'w+', newline='') as file:
        csv_writer = csv.writer(file)
        for array_line in array_of_users:
            csv_writer.writerow(array_line)

def create_room(room: Room, user: User):
    with open(db_rooms_path, 'a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([user.get_name(), room.get_unique_id(), room.get_password().decode()])

def leave_room(room_name: str, user: User):
    array_of_rooms_users = []

    with open(db_rooms_users_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if not (room_name.upper() == line[0].upper() and user.get_name().upper() == line[1].upper()):
                array_of_rooms_users.append(line)

    with open(db_rooms_users_path, 'w+', newline='') as file:
        csv_writer = csv.writer(file)
        for array_line in array_of_rooms_users:
            csv_writer.writerow(array_line)

def join_room_user(room_name, user: User):
    with open(db_rooms_users_path, 'a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([room_name, user.get_name()])
        #TODO SHOULD GIVE SOMETHING BACK TO CHECK IF JOINED
        #
        # if find_db_room_user():
        # return None


def get_my_rooms_that_i_joined(user: User):
    array_of_rooms = []

    with open(db_rooms_users_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if user.get_name().upper() == line[1].upper():

                room = find_db_room(line[0])
                array_of_rooms.append(room)

    return array_of_rooms

def get_my_rooms(user: User):
    array_of_rooms = []

    with open(db_rooms_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if user.get_name().upper() == line[0].upper():
                array_of_rooms.append(Room(line[1],line[2]))

    return array_of_rooms

def delete_my_room_connections(user: User):
    array_of_rooms_users = []
    with open(db_rooms_users_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if not user.get_name().upper() == line[1].upper():
                array_of_rooms_users.append(line)

    with open(db_rooms_users_path, 'w+', newline='') as file:
        csv_writer = csv.writer(file)
        for array_line in array_of_rooms_users:
            csv_writer.writerow(array_line)

def get_all_rooms(user: User):
    array_of_rooms = []

    with open(db_rooms_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if user.get_name().upper() == line[0].upper():
                array_of_rooms.append(Room(line[1],line[2]))

    with open(db_rooms_users_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if user.get_name().upper() == line[1].upper():
                # print(line[0],"dfdfddf")
                # szukaj pokoju zeby znalezc nazwe
                room = find_db_room(line[0])
                # print(room,"")

                array_of_rooms.append(room)

    return array_of_rooms

def check_if_already_joined_this_room(room_name, user: User):
    with open(db_rooms_users_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if room_name == line[0] and user.get_name().upper() == line[1].upper():
                #you joined this room before
                return True
        return False

def are_you_room_owner(user: User, room: Room):
    with open(db_rooms_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if user.get_name().upper() == line[0].upper() and room.get_unique_id().upper() == line[1].upper():
                #you are room owner
                return True
        return False

def check_room_data_to_delete(user: User, room_name, room_password):
    with open(db_rooms_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if user.get_name().upper() == line[0].upper() and room_name.upper() == line[1].upper() and bcrypt.checkpw(room_password.encode(), line[2].encode()):
                # you are room owner
                return True
        return False

def check_room_data_to_join(room_name, room_password):
    with open(db_rooms_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if room_name.upper() == line[1].upper() and bcrypt.checkpw(room_password.encode(), line[2].encode()):
                # data match
                return True
        return False


def delete_room(room: Room, user: User):
    array_of_rooms = []
    array_of_rooms_users = []

    #usuwamy w rooms i w rooms_users

    with open(db_rooms_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if not room.unique_id.upper() == line[1].upper():
                array_of_rooms.append(line)

    with open(db_rooms_path, 'w+', newline='') as file:
        csv_writer = csv.writer(file)
        for array_line in array_of_rooms:
            csv_writer.writerow(array_line)

    #rooms_users
    with open(db_rooms_users_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if not room.unique_id.upper() == line[0].upper():
                array_of_rooms_users.append(line)

    with open(db_rooms_users_path, 'w+', newline='') as file:
        csv_writer = csv.writer(file)
        for array_line in array_of_rooms_users:
            csv_writer.writerow(array_line)

def find_db_room(room_name):
    with open(db_rooms_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            #print(line[1].upper(), room_name.upper(),room_name.upper() == line[1].upper(),  " uuuuuuuuuuuuuuu")
            if room_name.upper() == line[1].upper():
                #print(line[1], " grrrrrrrrrrrr")
                return Room(line[1], line[2])
        return None