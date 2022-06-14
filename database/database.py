import bcrypt

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from database.user_model import User
from database.room_model import Room

class Database:

    def __init__(self, engine: Engine):
        self.engine: Engine = engine
        self.session: Session = sessionmaker(bind=engine)()

    # def check_db_exist(self, path):
    #     try:
    #         os.stat(path)
    #     except FileNotFoundError:
    #         f = open(path, "w")
    #         f.close()

    def write_db_user(self, user: User):
        self.session.add(user)
        self.session.commit()
        return user
        # self.cur.execute(
        #     "INSERT INTO user (name, password) "+
        #     "VALUES (? , ? )", (user.get_name(), user.get_password().decode()))
        # self.conn.commit()
        #
        # return self.cur.lastrowid

        # with open(db_users_path, 'a', newline='') as file:
        #     csv_writer = csv.writer(file)
        #     csv_writer.writerow([user.get_name(), user.get_password().decode()])

    def find_db_user_by_id(self, id):
        query = self.session.query(User)
        query = query.where(User.id == id)

        return query.first()

        # print(user_name)
        # self.cur.execute(" SELECT * FROM user WHERE user.id = ? ", [id])
        #
        # db_user = self.cur.fetchone()
        # print(db_user)
        # return self.make_user_object(db_user)

    def find_db_user(self, user_name: str):
        query = self.session.query(User)
        query = query.where(User.username == user_name)

        return query.first()

        #print(user_name)
        # self.cur.execute(" SELECT * FROM user WHERE name LIKE ? ", [user_name])
        #
        # db_user = self.cur.fetchone()
        #
        # #print(db_user)
        #
        # return self.make_user_object(db_user)

    # def make_user_object(self, db_user):
    #     if not db_user:
    #         return None
    #
    #     user = User(db_user[1], db_user[2].encode())
    #     user.set_id(db_user[0])
    #
    #     return user

    # def make_room_object(self, db_room):
    #     if not db_room:
    #         return None
    #
    #     #print(db_room)
    #
    #     room = Room(db_room[1], db_room[2], db_room[3].encode())
    #     room.set_id(db_room[0])
    #
    #     room.set_subject(db_room[4])
    #     #room.set_points(db_room[5])
    #
    #     return room
        #    print(user)
        #
        # with open(db_users_path, 'r', newline='') as file:
        #     csv_reader = csv.reader(file)
        #     for line in csv_reader:
        #          if user_name.upper() == line[0].upper():
        #             return User(line[0], line[1].encode())
        #     return None

    # def find_user_by_name(self, name):
    #     self.cur.execute("SELECT * FROM user WHERE name = ? AND hello = ?", (name, "world"))
    #     self.cur.fetchone()

    def find_db_all_users(self, filter_string):
        query = self.session.query(User)

        if len(filter_string) > 0:
            query = query.filter(User.username.like("%"+filter_string+"%"))

        for user in query.all():
            yield user


        # with open(db_users_path, 'r', newline='') as file:
        #     csv_reader = csv.reader(file)
        #     for line in csv_reader:
        #         if filter_string and filter_string.upper() in line[0].upper():
        #             print(line[0])
        #         elif not filter_string:
        #             print(line[0])

    def delete_db_user(self, user: User):
        rooms = []
        self.cur.execute("SELECT * FROM room WHERE owner_id = ?", [user.get_id()])

        for db_room in self.cur.fetchall():
            rooms.append(db_room[0])

        self.cur.execute("DELETE FROM room WHERE owner_id = ?", [user.get_id()])

        l = len(rooms)
        if l > 0:
            rooms.insert(0, user.get_id())
            self.cur.execute('DELETE FROM room_user WHERE user_id = ? OR room_id IN (%s)' % ','.join('?' * l), rooms)
        else:
            self.cur.execute("DELETE FROM room_user WHERE user_id = ?", [user.get_id()])

        self.cur.execute("DELETE FROM room_vote WHERE user_id = ?", [user.get_id()])

        self.cur.execute("DELETE FROM user WHERE id = ?", [user.get_id()])
        self.conn.commit()

        #array_of_users = []

        # with open(db_users_path, 'r', newline='') as file:
        #     csv_reader = csv.reader(file)
        #     for line in csv_reader:
        #         if not user.upper() == line[0].upper():
        #             array_of_users.append(line)
        #
        # with open(db_users_path, 'w+', newline='') as file:
        #     csv_writer = csv.writer(file)
        #     for array_line in array_of_users:
        #         csv_writer.writerow(array_line)

    def create_room(self, room: Room, user: User):
        self.session.add(room)
        room.users.append(user)
        self.session.commit()
        # self.cur.execute(
        #     "INSERT INTO room (owner_id, room_name, password, subject) " +
        #     "VALUES (?, ?, ? , '')", (user.get_id(), room.get_unique_id(), room.get_password().decode()))
        # self.conn.commit()
        #
        # return self.cur.lastrowid
        return room
        # with open(db_rooms_path, 'a', newline='') as file:
        #     csv_writer = csv.writer(file)
        #     csv_writer.writerow([user.get_name(), room.get_unique_id(), room.get_password().decode()])


    def leave_room_db(self, user_id, room_id):

        self.cur.execute("DELETE FROM room_user WHERE user_id = ? AND room_id = ? ", (user_id, room_id))

        self.cur.execute("DELETE FROM room_vote WHERE user_id = ? AND room_id = ? ", (user_id, room_id))

        self.conn.commit()

        #array_of_rooms_users = []

        # with open(db_rooms_users_path, 'r', newline='') as file:
        #     csv_reader = csv.reader(file)
        #     for line in csv_reader:
        #         if not (room_name.upper() == line[0].upper() and user.get_name().upper() == line[1].upper()):
        #             array_of_rooms_users.append(line)
        #
        # with open(db_rooms_users_path, 'w+', newline='') as file:
        #     csv_writer = csv.writer(file)
        #     for array_line in array_of_rooms_users:
        #         csv_writer.writerow(array_line)

    def join_room_user(self, room_id, user: User):
        query = self.session.query(Room).where(Room.id == room_id)

        room = query.first()

        if room and not room.users.filter(User.id == user.id).first():
            room.users.append(user)
            self.session.add(room)
            self.session.commit()
            return True
        return False

        # self.cur.execute(
        #     "INSERT INTO room_user (room_id, user_id) " +
        #     "VALUES (? , ? )", (room_id, user_id))
        # self.conn.commit()

        # with open(db_rooms_users_path, 'a', newline='') as file:
        #     csv_writer = csv.writer(file)
        #     csv_writer.writerow([room_name, user.get_name()])
        #     #TODO SHOULD GIVE SOMETHING BACK TO CHECK IF JOINED
            #
            # if find_db_room_user():
            # return None


    def get_my_rooms_that_i_joined(self, user: User):
        array_of_rooms = []

        with open(db_rooms_users_path, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            for line in csv_reader:
                if user.get_name().upper() == line[1].upper():

                    room = self.find_db_room(line[0])
                    array_of_rooms.append(room)

        return array_of_rooms

    def get_my_rooms_and_room_i_joined(self, user: User):
        query = self.session.query(Room)
        query = query.filter(
            Room.users.any(User.id == user.id)
        )

        #self.cur.execute(" SELECT r.id, u.name as owner_id, r.room_name, r.password, r.subject FROM room r INNER JOIN user u ON u.id = r.owner_id WHERE r.owner_id = ?  OR r.id IN (SELECT room_id FROM room_user ru WHERE  ru.user_id= ? )", [user.get_id(), user.get_id()])

        for room in query.all():
            #print(db_user)
            yield room


    def get_my_rooms(self, user: User):

        #self.cur.execute("SELECT * FROM  room WHERE name LIKE ?", ["%"+filter_string+"%"])

        for db_user in self.cur.fetchall():
            yield self.make_user_object(db_user)

        array_of_rooms = []

        with open(db_rooms_path, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            for line in csv_reader:
                if user.get_name().upper() == line[0].upper():
                    array_of_rooms.append(Room(line[1],line[2]))

        return array_of_rooms

    def delete_my_room_connections(self, user: User):
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

    def get_all_rooms(self, user: User):
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
                    room = self.find_db_room(line[0])
                    # print(room,"")

                    array_of_rooms.append(room)

        return array_of_rooms

    def check_if_already_joined_this_room_db(self, room_id, user: User):
        query = self.session.query(Room).where(Room.id == room_id)
        room = query.first()

        if room and room.users.filter(User.id == user.id).first():
            return True
        return False


        # self.cur.execute("SELECT * FROM room_user WHERE user_id = ? AND room_id = ?", (user_id, room_id))
        # record = self.cur.fetchone()
        #
        # if record is None:
        #     return False
        #
        # return True

    def is_subject_db(self, room_id):
        self.cur.execute("SELECT subject FROM room WHERE id  = ? ", [room_id])
        subject = self.cur.fetchone()

        if subject[0] and len(subject[0]) == 0:
            return False

        return True

    def set_subject_db(self, room_id, subject):
        self.cur.execute(
            "UPDATE room SET subject = ? " +
            " WHERE id = ?", (subject, room_id))

        self.cur.execute(
            "DELETE FROM room_vote " +
            " WHERE room_id = ?", (room_id))

        self.conn.commit()

        # with open(db_rooms_users_path, 'r', newline='') as file:
        #     csv_reader = csv.reader(file)
        #     for line in csv_reader:
        #         if room_name == line[0] and user.get_name().upper() == line[1].upper():
        #             #you joined this room before
        #             return True
        #     return False

    def is_point_db(self, room_id, user_id):
        self.cur.execute("SELECT vote FROM room_vote WHERE room_id  = ?  and user_id = ?", (room_id,user_id))
        vote = self.cur.fetchone()

        if vote:
            return True

        return False

    def add_points_db(self, room_id, user_id, points):
        # self.cur.execute(
        #     "UPDATE room SET points = points + ? " +
        #     " WHERE id = ?", (points, room_id))


        if(self.is_point_db(room_id, user_id)):
            self.cur.execute(
                "UPDATE room_vote SET vote = ? " +
                " WHERE room_id = ? and user_id = ?", (points, room_id, user_id))
        else:
            self.cur.execute(
                "INSERT INTO room_vote (room_id, user_id, vote) " +
                "VALUES (? , ? , ?)", (room_id, user_id, points))

        self.conn.commit()

        # with open(db_rooms_users_path, 'r', newline='') as file:
        #     csv_reader = csv.reader(file)
        #     for line in csv_reader:
        #         if room_name == line[0] and user.get_name().upper() == line[1].upper():
        #             #you joined this room before
        #             return True
        #     return False

    def check_room_data_to_delete(self, user: User, room_name, room_password):
        with open(db_rooms_path, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            for line in csv_reader:
                if user.get_name().upper() == line[0].upper() and room_name.upper() == line[1].upper() and bcrypt.checkpw(room_password.encode(), line[2].encode()):
                    # you are room owner
                    return True
            return False

    def check_room_data_to_join(self, room_name, room_password):
        with open(db_rooms_path, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            for line in csv_reader:
                if room_name.upper() == line[1].upper() and bcrypt.checkpw(room_password.encode(), line[2].encode()):
                    # data match
                    return True
            return False


    def delete_room_db(self, room: Room, user: User):

        self.cur.execute("DELETE FROM room WHERE id = ?", [room.id])

        self.cur.execute("DELETE FROM room_user WHERE room_id = ?", [room.id])

        self.cur.execute("DELETE FROM room_vote WHERE room_id = ?", [room.id])

        self.conn.commit()

        # array_of_rooms = []
        # array_of_rooms_users = []

        #usuwamy w rooms i w rooms_users

        # with open(db_rooms_path, 'r', newline='') as file:
        #     csv_reader = csv.reader(file)
        #     for line in csv_reader:
        #         if not room.unique_id.upper() == line[1].upper():
        #             array_of_rooms.append(line)
        #
        # with open(db_rooms_path, 'w+', newline='') as file:
        #     csv_writer = csv.writer(file)
        #     for array_line in array_of_rooms:
        #         csv_writer.writerow(array_line)
        #
        # #rooms_users
        # with open(db_rooms_users_path, 'r', newline='') as file:
        #     csv_reader = csv.reader(file)
        #     for line in csv_reader:
        #         if not room.unique_id.upper() == line[0].upper():
        #             array_of_rooms_users.append(line)
        #
        # with open(db_rooms_users_path, 'w+', newline='') as file:
        #     csv_writer = csv.writer(file)
        #     for array_line in array_of_rooms_users:
        #         csv_writer.writerow(array_line)

    def find_db_room_users(self, room_id):
        self.cur.execute(" SELECT * FROM user WHERE "
                         "id in( SELECT user_id from room_user where room_id = ? )  or "
                         "id in ( SELECT owner_id from room where id = ? ) ", (room_id, room_id))

        for db_user in self.cur.fetchall():
            yield self.make_user_object(db_user)


    def find_db_room(self, room_name):
        query = self.session.query(Room)
        query = query.where(Room.name == room_name)

        return query.first()
        # owner_id
        # INTEGER, room_name
        # TEXT, password
        # TEXT
        # self.cur.execute(" SELECT * FROM room WHERE room_name LIKE ? ", [room_name])
        #
        # db_room = self.cur.fetchone()
        #
        # # print(db_user)
        #
        # return self.make_room_object(db_room)

    def get_room_votes(self, room_id):
        self.cur.execute(" SELECT user.name, room_vote.vote FROM room_vote "
                         "INNER JOIN user ON user.id = room_vote.user_id WHERE room_id = ? ", [room_id])

        for row in self.cur.fetchall():
            yield {'username': row[0], 'value': row[1]}

    def update_room_db(self, room: Room):
        old_room = self.find_db_room_by_id(room.id)

        self.cur.execute(" UPDATE room set subject = ?, password = ? WHERE id = ? ",
                         (room.get_subject(), room.get_password().decode(), room.id))

        if old_room.get_subject() != room.get_subject():
            self.cur.execute(" DELETE FROM room_vote WHERE room_id = ? ", [room.id])

        self.conn.commit()

    def find_db_room_by_id(self, room_id):
        query = self.session.query(Room)
        query = query.where(Room.id == room_id)
        # self.cur.execute(" SELECT * FROM room WHERE id = ? ", [room_id])
        #
        # db_room = self.cur.fetchone()
        #
        # print(db_room)

        #return self.make_room_object(db_room)
        return query.first()

        # with open(db_rooms_path, 'r', newline='') as file:
        #     csv_reader = csv.reader(file)
        #     for line in csv_reader:
        #         #print(line[1].upper(), room_name.upper(),room_name.upper() == line[1].upper(),  " uuuuuuuuuuuuuuu")
        #         if room_name.upper() == line[1].upper():
        #             #print(line[1], " grrrrrrrrrrrr")
        #             return Room(line[1], line[2])
        #     return None

    def get_user(self):
        self.cur.execute("SELECT * FROM user;")
        for user in self.cur.fetchall():
            print(user)

    # def create_tables(self):
    #     self.cur.execute(
    #         "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT);")
    #     self.cur.execute(
    #         "CREATE TABLE IF NOT EXISTS room_vote (id INTEGER PRIMARY KEY AUTOINCREMENT, room_id INTEGER, user_id INTEGER, vote NUMERIC);")
    #     self.cur.execute(
    #         "CREATE TABLE IF NOT EXISTS room (id INTEGER PRIMARY KEY AUTOINCREMENT, owner_id INTEGER, room_name TEXT, password TEXT, subject TEXT);")
    #     self.cur.execute("CREATE TABLE IF NOT EXISTS room_user (room_id INTEGER, user_id INTEGER);")
    #     #self.cur.execute("INSERT INTO user (name, password) VALUES ('Fancia', 'password')")
    #     self.conn.commit()

    # def delete_tables(self):
    #     self.cur.execute("DROP TABLE IF EXISTS user;")
    #     self.cur.execute("DROP TABLE IF EXISTS room;")
    #     self.cur.execute("DROP TABLE IF EXISTS room_user;")
    #     self.cur.execute("DROP TABLE IF EXISTS room_vote;")
    #     self.conn.commit()
    #
    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def delete_tables(self):
        Base.metadata.drop_all(self.engine)

def get_database(filepath):
    engine = create_engine("sqlite:///{}".format(filepath), echo=True)
    return Database(engine)

