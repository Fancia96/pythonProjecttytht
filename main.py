# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

import click
import uvicorn

import commands.usersCommands
import config
import getpass

from database.user_model import User
from database.room_model import Room
from expections.expections import Expection
from users.users_service import UserService
from rooms.rooms_service import RoomsService

user_service = UserService()
rooms_service = RoomsService()




@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = {}
    ctx.obj['db'] = config.db

@cli.command()
@click.pass_obj
def run_as_server(ctx):
    uvicorn.run("server:app", host="127.0.0.1", port=5000, log_level="info")

@cli.command()
@click.pass_obj
def initialize_db(obj):

    obj['db'].delete_tables()

    obj['db'].create_tables()

    print("Baza danych zresetowana")

@cli.group('user')
@click.option("--login", required=True)
@click.password_option(confirmation_prompt=False)
@click.pass_obj
def user(obj, login, password):
    db = obj['db']

    user = commands.usersCommands.login(db, login, password)
    #user = user_service.login(db, login, password)
    if user is None:
        print("Nieprawidłowy login lub hasło")
        sys.exit()
        #raise Exception("Nieprawidłowy login lub hasło")
    else:
        print("Zalogowano")
        obj['user'] = user

@cli.command()
@click.option("--register_name", required=True)
@click.password_option(confirmation_prompt=False)
@click.pass_obj
def register(obj, register_name, password):
    db = obj['db']
    #print(db)
    #user_service.find_all_users(db)
    try:
        user = commands.usersCommands.register(db, register_name, password)
        obj['user'] = user
        click.echo("Zarejestrowano użytkownika")
    except Expection as exp:
        print(exp.massage)

#bez filtra pokazuje wszystkich, z nim filtruje
@user.command()
@click.pass_obj
@click.option("--filter", required=False)
def show_users(obj, filter):
    #show_users
    db = obj['db']
    #user = obj['user']

    users_list = user_service.find_all_users(db, filter)

    for user in users_list:
        click.echo(user.get_name())


@user.command()
@click.pass_obj
@click.option("--im_sure", required=False, is_flag=True, default=False)
def delete_yourself(obj, im_sure):
    db = obj['db']
    user = obj['user']

    if im_sure:
        user = user_service.delete_user(db, user)

        if user is None:
            print("Usunięto użytkownika")
        else:
            print("Nie usunięto użytkownika")
            sys.exit()
    else:
        print("Nie usunięto użytkownika")
        sys.exit()

@user.command()
@click.pass_obj
@click.option("--unique_id", required=True)
@click.password_option(confirmation_prompt=False)
def create_room(obj, unique_id, password):
    db = obj['db']
    user = obj['user']

    if rooms_service.check_room_name(db, unique_id, True):
        #print("Haslo co najmniej 8 znaków, duże i małe litery, cyfry i znaki specjalne")
        #_ask_for_room_password()
        if user_service.check_password(password):
            room = rooms_service.create_room(db, user, unique_id, password)
            if room:
                print("Pokój został utworzony")
                room = None
            else:
                print("")


@user.group('room')
@click.option("--unique_id", required=True)
#@click.password_option(confirmation_prompt=False)
@click.pass_obj
def room(obj, unique_id):
    #vrerify blablabla
    user = obj['user']
    db = obj['db']

    room: Room = rooms_service.find_room(obj['db'], unique_id, '', False)
    if room is None:
        print("Nieprawidłowa nazwa lub hasło pokoju")
        sys.exit()
        #raise Exception("Nieprawidłowy login lub hasło")
    else:
        if rooms_service.check_if_already_joined_this_room(db, room.get_id(), user.get_id()) or rooms_service.are_you_room_owner(user.get_id(), room.get_owner_id()):
            print("Prawidłowe dane pokoju")
            obj['room'] = room
        else:
            password = getpass.getpass("Podaj haslo do pokoju: ")
            room_2: Room = rooms_service.find_room(obj['db'], unique_id, password, True)
            if room_2 is None:
                print("Nieprawidłowa nazwa lub hasło pokoju")
                sys.exit()
            else:
                print("Prawidłowe dane pokoju")

                joined = rooms_service.join_room(db, room_2.get_id(), user.get_id())

                if joined:
                    print("Dołączono do pokoju")
                else:
                    print("Nie dołączono do pokoju")
                    sys.exit()

                obj['room'] = room_2



@room.command()
@click.option("--im_sure", required=False, is_flag=True, default=False)
@click.pass_obj
def delete_room(obj, im_sure):
    # check if you are owner
    room = rooms_service.delete_room(obj['db'], obj['room'], obj['user'])

    if room is None:
        print("Pokój został usunięty")
    else:
        print("Nie usunięto pokoju")


@room.command()
@click.pass_obj
def join_room(obj):

    pass
#     db = obj['db']
#     room = obj['room']
#     user = obj['user']
#
#     # check if you are owner
#     if not rooms_service.are_you_room_owner(user.get_id(), room.get_owner_id()):
#
#         # check if you already joned this room
#         if not rooms_service.check_if_already_joined_this_room(db, room.get_id(), user.get_id()):
#
#             joined = rooms_service.join_room(db, room.get_id(), user.get_id())
#
#             if joined:
#                 print("Dołączono do pokoju")
#             else:
#                 print("Nie dołączono do pokoju")
#         else:
#             print("Już dołączyłeś do tego pokoju wcześniej")
#     else:
#         print("Nie jesteś wlascicielem pokoju")


@room.command()
@click.pass_obj
def leave_room(obj):
    db = obj['db']
    room = obj['room']
    user = obj['user']

    # check if you are owner
    if not rooms_service.are_you_room_owner(user.get_id(), room.get_owner_id()):

        # check if you already joned this room
        if rooms_service.check_if_already_joined_this_room(db, room.get_id(), user.get_id()):

            left_room = rooms_service.leave_room(db, user.get_id(), room.get_id())

            if not left_room:
                print("Opuszczono pokój")
            else:
                print("Nie opuszczono do pokoju")

        else:
            print("Nie przynależysz do tego pokoju")
    else:
        print("Jesteś właścicielem podanego pokoju więc nie możesz go opuścić, możesz go usunąć")


#TODO SHHHHHHHHHHHHHHHHHHHHHHH
    #shh_all_rooms


@room.group('subject')
@click.pass_obj
def subject(obj):
    pass

@subject.command()
@click.option("--subject", required=True)
@click.pass_obj
def set(obj, subject):
    db = obj['db']
    room = obj['room']
    user = obj['user']

    # check if you are owner
    if rooms_service.are_you_room_owner(user.get_id(), room.get_owner_id()):

        #is_subject = rooms_service.is_subject(db, room.get_id())

        complete = rooms_service.set_subject(db, room.get_id(), subject)
        if complete:
            print("Temat ustawiony")
    else:
        print("Nie jesteś wlascicielem pokoju")

# @subject.command()
# @click.pass_obj
# def set_active_subject(obj):
#
#     pass

@subject.command()
@click.option("--im_sure", required=False, is_flag=True, default=False)
@click.pass_obj
def delete(obj, im_sure):
    db = obj['db']
    room = obj['room']
    user = obj['user']

    # check if you are owner
    if rooms_service.are_you_room_owner(user.get_id(), room.get_owner_id()):

        complete = rooms_service.set_subject(db, room.get_id(), '')
        if complete:
            print("Temat usunięty")
    else:
        print("Nie jesteś wlascicielem pokoju")

@subject.command()
@click.option("--number", required=True, type=float)
@click.pass_obj
def vote(obj, number):
    db = obj['db']
    room = obj['room']
    user = obj['user']

    list = [0, 0.5, 1, 2, 3, 5, 8, 13, 20, 50, 100, 200, -1, -2]

    if number in list:
        points = rooms_service.add_points(db, room.get_id(), user.get_id(), number)
        print(f"Punkty dodane - aktualne {points}")
    else:
        print(f"ZŁY NUMER {number} Można głosowac jedynie podajać poniższe wartości")
        print(", ".join(str(item) for item in list))



# def main_menu():
#     global user
#     os.system('cls')
#     print("Witam - oto ekran powitalny")
#     print("Zaloguj - opcja 1")
#     print("Zarejestruj - opcja 2")
#
#     opcja = input("Opcja:")
#
#     if opcja == "1":
#         login()
#     elif opcja == "2":
#         register()
#     elif opcja == "666":
#         user = User("Fancia", "Abc123@@@")
#         menu()
#     else:
#         print("Złe hasło")
#         _ask_for_enter()
#         main_menu()

#
# def menu():
#     global user
#     global room
#     os.system('cls')
#
#     print("Jestes zalogowany jako ", user.get_name())
#     print("")
#     print("Co chcesz zrobic?")
#     print("")
#     print("Wylistuj wszystkich użytkowników - opcja 1")
#     print("Filtruj użytkowników - opcja 2")
#     print("Usuń swojego użytkownika - opcja 3")
#
#     print("Pokoje - opcja 4")
#
#     print("Wyloguj - opcja 5")
#     opcja = input("Opcja:")
#
#     if opcja == "1":
#         database.database.find_db_all_users("")
#
#         _ask_for_enter()
#
#         menu()
#     elif opcja == "2":
#         print("Wpisz tekst dla filtrowania (wielkość liter nie ma znaczenia) ")
#         filter_string = input("")
#         database.database.find_db_all_users(filter_string)
#
#         _ask_for_enter()
#
#         menu()
#     elif opcja == "3":
#         print("Usunąć? ", user.get_name(), " y / n ?")
#         delete = input("")
#
#         if delete.upper() == "Y":
#             user = user_service.delete_user(user)
#
#             if user is None:
#                 main_menu()
#             else:
#                 print("Nie usunięto użytkownika")
#                 _ask_for_enter()
#                 menu()
#         else:
#             menu()
#     elif opcja == "4":
#         rooms()
#     elif opcja == "5":
#         user = None
#         main_menu()
#     else:
#         print("Zła opcja")
#         _ask_for_enter()
#         menu()


# def user():
#     os.system('cls')
#
#     print("Zaloguj się")
#
#     _ask_for_name()
#     _ask_for_password()
#     user = user_service.login(name, password)
#     if user is None:
#         print("Nieprawidłowy login lub hasło")
#         _ask_for_enter()
#         main_menu()
#     else:
#        menu()

# def login():
#     global user
#     os.system('cls')
#
#     print("Zaloguj się")
#
#     _ask_for_name()
#     _ask_for_password()
#     user = user_service.login(name, password)
#     if user is None:
#         print("Nieprawidłowy login lub hasło")
#         _ask_for_enter()
#         main_menu()
#     else:
#         menu()

#
# def rooms():
#     global user
#     global room
#     os.system('cls')
#
#     print("Jestes zalogowany jako ", user.get_name())
#     print("MENU POKOJE")
#
#     print("")
#     print("Co chcesz zrobic?")
#     print("")
#     print("Utwórz własny pokój - opcja 1")
#     print("Usuń własny pokój - opcja 2")
#     print("Dołącz do innego pokoju - opcja 3")
#     print("Opuść inny pokój - opcja 4");
#     print("Wyświetl wszystkie pokoje - opcja 5")
#
#     print("Powrót - opcja 6")
#     opcja = input("Opcja:")
#
#     if opcja == "1":
#         os.system('cls')
#         print("TWORZENIE POKOJU")
#
#         room = None
#         # while room is None:
#         _ask_for_room_name()
#         if rooms_service.check_room_name(room_name, True):
#             print("Haslo co najmniej 8 znaków, duże i małe litery, cyfry i znaki specjalne")
#             _ask_for_room_password()
#             if user_service.check_password(room_password):
#                 room = rooms_service.create_room(user, room_name, room_password)
#                 if room:
#                     print("Pokój został utworzony")
#                     room = None
#
#         _ask_for_enter()
#         rooms()
#
#
#
#     elif opcja == "2":
#         os.system('cls')
#         print("USUWANIE POKOJU")
#
#         print("TWOJE UTWORZONE POKOJE")
#         my_rooms = []
#
#         for room in database.database.get_my_rooms(user):
#             my_rooms.append(room)
#
#         for room in my_rooms:
#             print(room.get_unique_id())
#
#         _ask_for_room_name()
#         #
#         if rooms_service.check_room_name(room_name, False):
#
#             room = database.database.find_db_room(room_name)
#
#             # if room exists
#             if room:
#
#                 # check if you are owner
#                 if database.database.are_you_room_owner(user, room):
#
#                     print("Podaj hasło w celu usunięcia pokoju")
#                     _ask_for_room_password()
#                     # get whole acceptance to delete
#                     if database.database.check_room_data_to_delete(user, room_name, room_password):
#
#                         print("Usunąć pokój? ", room.unique_id, " y / n ?")
#                         delete = input("")
#
#                         if delete.upper() == "Y":
#                             room = rooms_service.delete_room(room, user)
#
#                             if room is None:
#                                 print("Pokój został usunięty")
#                                 _ask_for_enter()
#                                 rooms()
#                             else:
#                                 print("Nie usunięto pokoju")
#                                 _ask_for_enter()
#                                 rooms()
#                         else:
#                             rooms()
#                     else:
#                         print("Nie podałes prawidłowych danych pokoju - nie usunięto")
#                         _ask_for_enter()
#                         rooms()
#                 else:
#                     print("Nie jesteś właścicielem podanego pokoju")
#                     _ask_for_enter()
#                     rooms()
#             else:
#                 print("Podana nazwa pokoju nie istnieje")
#                 _ask_for_enter()
#                 rooms()
#         else:
#             _ask_for_enter()
#             rooms()
#
#     elif opcja == "3":
#         os.system('cls')
#         print("DOŁĄCZANIE DO INNEGO POKOJU")
#
#         _ask_for_room_name()
#
#         if rooms_service.check_room_name(room_name, False):
#
#             # if room exists
#             room = database.database.find_db_room(room_name)
#             if room:
#
#                 # check if you are owner
#                 if not database.database.are_you_room_owner(user, room):
#
#                     # check if you already joned this room
#                     if not database.database.check_if_already_joined_this_room(room_name, user):
#
#                         print("Podaj hasło w celu dołączenia do pokoju")
#                         _ask_for_room_password()
#                         # get whole acceptance to delete
#                         if database.database.check_room_data_to_join(room_name, room_password):
#
#                             joined = rooms_service.join_room(room_name, user)
#
#                             if joined:
#                                 print("Dołączono do pokoju")
#                                 _ask_for_enter()
#                                 rooms()
#                             else:
#                                 print("Nie dołączono do pokoju")
#                                 _ask_for_enter()
#                                 rooms()
#
#                         else:
#                             print("Nie podałes prawidłowych danych pokoju - nie dołączono")
#                             _ask_for_enter()
#                             rooms()
#                     else:
#                         print("Juz przynależysz do tego pokoju")
#                         _ask_for_enter()
#                         rooms()
#                 else:
#                     print("Jesteś właścicielem podanego pokoju więc nie możesz już dołączyć!")
#                     _ask_for_enter()
#                     rooms()
#             else:
#                 print("Podana nazwa pokoju nie istnieje")
#                 _ask_for_enter()
#                 rooms()
#         else:
#             _ask_for_enter()
#             rooms()
#     elif opcja == "4":
#         os.system('cls')
#         print("OPCJA OPUSZCZENIA POKOJU")
#
#         print("--- POKOJE DO KTORYCH DOLACZYLES ---")
#         my_rooms = []
#
#         for room in database.database.get_my_rooms_that_i_joined(user):
#             my_rooms.append(room)
#
#         for room in my_rooms:
#             print(room.get_unique_id())
#
#         _ask_for_room_name()
#         if rooms_service.check_room_name(room_name, False):
#
#             # if room exists
#             room = database.database.find_db_room(room_name)
#             if room:
#
#                 # check if you are owner
#                 if not database.database.are_you_room_owner(user, room):
#
#                     # check if you already joned this room
#                     if database.database.check_if_already_joined_this_room(room_name, user):
#
#                         left_room = rooms_service.leave_room(room_name, user)
#
#                         if not left_room:
#                             print("Opuszczono pokój")
#                             _ask_for_enter()
#                             rooms()
#                         else:
#                             print("Nie opuszczono do pokoju")
#                             _ask_for_enter()
#                             rooms()
#
#                         _ask_for_enter()
#                         rooms()
#                     else:
#                         print("Nie przynależysz do tego pokoju")
#                         _ask_for_enter()
#                         rooms()
#                 else:
#                     print("Jesteś właścicielem podanego pokoju więc nie możesz go opuścić, możesz go usunąć")
#                     _ask_for_enter()
#                     rooms()
#             else:
#                 print("Podana nazwa pokoju nie istnieje")
#                 _ask_for_enter()
#                 rooms()
#         else:
#             _ask_for_enter()
#             rooms()
#     elif opcja == "5":
#         os.system('cls')
#         print("TWOJE POKOJE")
#
#         print("--- TWOJE UTWORZONE POKOJE ---")
#         for room in database.database.get_my_rooms(user):
#             print(room.get_unique_id())
#
#         print("--- POKOJE DO KTORYCH DOLACZYLES ---")
#         for room in database.database.get_my_rooms_that_i_joined(user):
#             print(room.get_unique_id())
#
#         # my_rooms.extend(database.database.get_rooms_im_in(user))
#
#         #for room in my_rooms:
#         #   print(room.get_unique_id())
#
#         _ask_for_enter()
#         rooms()
#
#     elif opcja == "6":
#         menu()
#     else:
#         print("Zła opcja")
#         _ask_for_enter()
#         rooms()


# def register():
#     global user
#
#     user_service.register_user()# przemienic metodki
#
#     os.system('cls')
#     print("Zarejestruj się")
#     print("Nazwa uzytkownika")
#
#     _ask_for_name()
#     if user_service.check_name(name):
#         print("Haslo co najmniej 8 znaków, duże i małe litery, cyfry i znaki specjalne")
#         _ask_for_password()
#         if user_service.check_password(password):
#             user = user_service.register(name, password)
#     if user is None:
#         _ask_for_enter()
#         main_menu()
#     else:
#         menu()


# def _ask_for_name():
#     global name
#     name = input("Podaj nazwe uzytkownika: ")
#
#
# def _ask_for_enter():
#     print("Powrót do menu, naciśnij enter ")
#     powrot = input("")
#
#
# def _ask_for_password():
#     global password
#     password = getpass.getpass("Podaj haslo: ")
#
#
# def _ask_for_room_name():
#     global room_name
#     room_name = input("Podaj nazwe pokoju: ")
#
#
# def _ask_for_room_password():
#     global room_password
#     room_password = getpass.getpass("Podaj haslo pokoju: ")


if __name__ == '__main__':
    cli()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
