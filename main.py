# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import typing

import database.database
import os
import getpass

from database.user_model import User
from database.room_model import Room
from users.users_service import UserService
from rooms.rooms_service import RoomsService

name = ""
password = ""

room_name = ""
room_password = ""

user: typing.Union[User, None] = None
room: typing.Union[Room, None] = None

user_service = UserService()
rooms_service = RoomsService()


def main_menu():
    global user
    os.system('cls')
    print("Witam - oto ekran powitalny")
    print("Zaloguj - opcja 1")
    print("Zarejestruj - opcja 2")

    opcja = input("Opcja:")

    if opcja == "1":
        login()
    elif opcja == "2":
        register()
    elif opcja == "666":
        user = User("Fancia", "Abc123@@@")
        menu()
    else:
        print("Złe hasło")
        _ask_for_enter()
        main_menu()


def menu():
    global user
    global room
    os.system('cls')

    print("Jestes zalogowany jako ", user.get_name())
    print("")
    print("Co chcesz zrobic?")
    print("")
    print("Wylistuj wszystkich użytkowników - opcja 1")
    print("Filtruj użytkowników - opcja 2")
    print("Usuń swojego użytkownika - opcja 3")

    print("Pokoje - opcja 4")

    print("Wyloguj - opcja 5")
    opcja = input("Opcja:")

    if opcja == "1":
        database.database.find_db_all_users("")

        _ask_for_enter()

        menu()
    elif opcja == "2":
        print("Wpisz tekst dla filtrowania (wielkość liter nie ma znaczenia) ")
        filter_string = input("")
        database.database.find_db_all_users(filter_string)

        _ask_for_enter()

        menu()
    elif opcja == "3":
        print("Usunąć? ", user.get_name(), " y / n ?")
        delete = input("")

        if delete.upper() == "Y":
            user = user_service.delete_user(user)

            if user is None:
                main_menu()
            else:
                print("Nie usunięto użytkownika")
                _ask_for_enter()
                menu()
        else:
            menu()
    elif opcja == "4":
        rooms()
    elif opcja == "5":
        user = None
        main_menu()
    else:
        print("Zła opcja")
        _ask_for_enter()
        menu()


def login():
    global user
    os.system('cls')

    print("Zaloguj się")

    _ask_for_name()
    _ask_for_password()
    user = user_service.login(name, password)
    if user is None:
        print("Nieprawidłowy login lub hasło")
        _ask_for_enter()
        main_menu()
    else:
        menu()


def rooms():
    global user
    global room
    os.system('cls')

    print("Jestes zalogowany jako ", user.get_name())
    print("MENU POKOJE")

    print("")
    print("Co chcesz zrobic?")
    print("")
    print("Utwórz własny pokój - opcja 1")
    print("Usuń własny pokój - opcja 2")
    print("Dołącz do innego pokoju - opcja 3")
    print("Opuść inny pokój - opcja 4");
    print("Wyświetl wszystkie pokoje - opcja 5")

    print("Powrót - opcja 6")
    opcja = input("Opcja:")

    if opcja == "1":
        os.system('cls')
        print("TWORZENIE POKOJU")

        room = None
        # while room is None:
        _ask_for_room_name()
        if rooms_service.check_room_name(room_name, True):
            print("Haslo co najmniej 8 znaków, duże i małe litery, cyfry i znaki specjalne")
            _ask_for_room_password()
            if user_service.check_password(room_password):
                room = rooms_service.create_room(user, room_name, room_password)
                if room:
                    print("Pokój został utworzony")
                    room = None

        _ask_for_enter()
        rooms()



    elif opcja == "2":
        os.system('cls')
        print("USUWANIE POKOJU")

        print("TWOJE UTWORZONE POKOJE")
        my_rooms = []

        for room in database.database.get_my_rooms(user):
            my_rooms.append(room)

        for room in my_rooms:
            print(room.get_unique_id())

        _ask_for_room_name()
        #
        if rooms_service.check_room_name(room_name, False):

            room = database.database.find_db_room(room_name)

            # if room exists
            if room:

                # check if you are owner
                if database.database.are_you_room_owner(user, room):

                    print("Podaj hasło w celu usunięcia pokoju")
                    _ask_for_room_password()
                    # get whole acceptance to delete
                    if database.database.check_room_data_to_delete(user, room_name, room_password):

                        print("Usunąć pokój? ", room.unique_id, " y / n ?")
                        delete = input("")

                        if delete.upper() == "Y":
                            room = rooms_service.delete_room(room, user)

                            if room is None:
                                print("Pokój został usunięty")
                                _ask_for_enter()
                                rooms()
                            else:
                                print("Nie usunięto pokoju")
                                _ask_for_enter()
                                rooms()
                        else:
                            rooms()
                    else:
                        print("Nie podałes prawidłowych danych pokoju - nie usunięto")
                        _ask_for_enter()
                        rooms()
                else:
                    print("Nie jesteś właścicielem podanego pokoju")
                    _ask_for_enter()
                    rooms()
            else:
                print("Podana nazwa pokoju nie istnieje")
                _ask_for_enter()
                rooms()
        else:
            _ask_for_enter()
            rooms()

    elif opcja == "3":
        os.system('cls')
        print("DOŁĄCZANIE DO INNEGO POKOJU")

        _ask_for_room_name()

        if rooms_service.check_room_name(room_name, False):

            # if room exists
            room = database.database.find_db_room(room_name)
            if room:

                # check if you are owner
                if not database.database.are_you_room_owner(user, room):

                    # check if you already joned this room
                    if not database.database.check_if_already_joined_this_room(room_name, user):

                        print("Podaj hasło w celu dołączenia do pokoju")
                        _ask_for_room_password()
                        # get whole acceptance to delete
                        if database.database.check_room_data_to_join(room_name, room_password):

                            joined = rooms_service.join_room(room_name, user)

                            if joined:
                                print("Dołączono do pokoju")
                                _ask_for_enter()
                                rooms()
                            else:
                                print("Nie dołączono do pokoju")
                                _ask_for_enter()
                                rooms()

                        else:
                            print("Nie podałes prawidłowych danych pokoju - nie dołączono")
                            _ask_for_enter()
                            rooms()
                    else:
                        print("Juz przynależysz do tego pokoju")
                        _ask_for_enter()
                        rooms()
                else:
                    print("Jesteś właścicielem podanego pokoju więc nie możesz już dołączyć!")
                    _ask_for_enter()
                    rooms()
            else:
                print("Podana nazwa pokoju nie istnieje")
                _ask_for_enter()
                rooms()
        else:
            _ask_for_enter()
            rooms()
    elif opcja == "4":
        os.system('cls')
        print("OPCJA OPUSZCZENIA POKOJU")

        print("--- POKOJE DO KTORYCH DOLACZYLES ---")
        my_rooms = []

        for room in database.database.get_my_rooms_that_i_joined(user):
            my_rooms.append(room)

        for room in my_rooms:
            print(room.get_unique_id())

        _ask_for_room_name()
        if rooms_service.check_room_name(room_name, False):

            # if room exists
            room = database.database.find_db_room(room_name)
            if room:

                # check if you are owner
                if not database.database.are_you_room_owner(user, room):

                    # check if you already joned this room
                    if database.database.check_if_already_joined_this_room(room_name, user):

                        left_room = rooms_service.leave_room(room_name, user)

                        if not left_room:
                            print("Opuszczono pokój")
                            _ask_for_enter()
                            rooms()
                        else:
                            print("Nie opuszczono do pokoju")
                            _ask_for_enter()
                            rooms()

                        _ask_for_enter()
                        rooms()
                    else:
                        print("Nie przynależysz do tego pokoju")
                        _ask_for_enter()
                        rooms()
                else:
                    print("Jesteś właścicielem podanego pokoju więc nie możesz go opuścić, możesz go usunąć")
                    _ask_for_enter()
                    rooms()
            else:
                print("Podana nazwa pokoju nie istnieje")
                _ask_for_enter()
                rooms()
        else:
            _ask_for_enter()
            rooms()
    elif opcja == "5":
        os.system('cls')
        print("TWOJE POKOJE")

        print("--- TWOJE UTWORZONE POKOJE ---")
        for room in database.database.get_my_rooms(user):
            print(room.get_unique_id())

        print("--- POKOJE DO KTORYCH DOLACZYLES ---")
        for room in database.database.get_my_rooms_that_i_joined(user):
            print(room.get_unique_id())

        # my_rooms.extend(database.database.get_rooms_im_in(user))

        #for room in my_rooms:
        #   print(room.get_unique_id())

        _ask_for_enter()
        rooms()

    elif opcja == "6":
        menu()
    else:
        print("Zła opcja")
        _ask_for_enter()
        rooms()


def register():
    global user
    os.system('cls')
    print("Zarejestruj się")
    print("Nazwa uzytkownika")

    _ask_for_name()
    if user_service.check_name(name):
        print("Haslo co najmniej 8 znaków, duże i małe litery, cyfry i znaki specjalne")
        _ask_for_password()
        if user_service.check_password(password):
            user = user_service.register(name, password)
    if user is None:
        _ask_for_enter()
        main_menu()
    else:
        menu()


def _ask_for_name():
    global name
    name = input("Podaj nazwe uzytkownika: ")


def _ask_for_enter():
    print("Powrót do menu, naciśnij enter ")
    powrot = input("")


def _ask_for_password():
    global password
    password = getpass.getpass("Podaj haslo: ")

if __name__ == '__main__':
    main_menu()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
