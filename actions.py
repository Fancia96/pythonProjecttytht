import getpass
import os

import database


class Actions:
    def __init__(self):
        database.check_db_exist(database.db_path)
        self.name = ""
        self.password = ""

    def main_menu(self):
        os.system('cls')
        print("Witam - oto ekran powitalny")
        print("Zaloguj - opcja 1")
        print("Zarejestruj - opcja 2")

        opcja = input("")

        if opcja == "1":
            self.login()
        elif opcja == "2":
            self.register()
        else:
            print("Złe hasło")

    def login(self):
        os.system('cls')

        print("Zaloguj się")

        self._ask_for_name()

        bad_name = True

        while bad_name:
            if database.find_db_user(self.name, self.password, False):
                # tu mam nazwe, git next
                bad_name = False
            else:
                self._ask_for_name()

        self._ask_for_password()

        if database.find_db_user(self.name, self.password, True):
            self.menu()
        else:
            print("Podałeś złe hasło")

            self._ask_for_enter()

            self.main_menu()

    def register(self):
        os.system('cls')
        print("Zarejestruj się")
        print("Nazwa uzytkownika")
        self._ask_for_name()

        bad_name = True

        while bad_name:
            alpha_numeric = "abcdefghijklmnopqrstuvwxyz0123456789"

            if len(self.name) == 0:
                print("Nazwa nie może być pusta")
                self._ask_for_name()
            elif not all(c in alpha_numeric for c in self.name.lower()):
                print("Nazwa musi składać się z liter a-z oraz numerow 0-9 oraz nie zawierac spacji")
                self._ask_for_name()
            elif database.find_db_user(self.name, self.password, False):
                print("Podana nazwa użytkownika już istnieje")
                self._ask_for_name()
            else:
                bad_name = False

        print("Haslo co najmniej 8 znaków, duże i małe litery, cyfry i znaki specjalne")
        self._ask_for_password()

        bad_password = True
        while bad_password:
            bad_password_length = True
            bad_password_small_letter = True
            bad_password_big_letter = True
            bad_password_numbers = True
            bad_password_specials = True

            special_characters = "!@#$%^&*()-+?_=,.{}\<>/"

            if len(self.password) < 8:
                print("haslo za krotkie")
                bad_password_length = False
            if not any(char.isdigit() for char in self.password):
                print("haslo musi zawierać cyfrę")
                bad_password_numbers = False
            if self.password.upper() == self.password:
                print("haslo musi zawierać małe litery")
                bad_password_small_letter = False
            if self.password.lower() == self.password:
                print("haslo musi zawierać duże litery")
                bad_password_big_letter = False
            if not any(c in special_characters for c in self.password):
                print("haslo musi zawierać znak specjalny")
                bad_password_specials = False
            if ' ' in self.password == True:
                print("haslo nie moze zawierac spacji")
                bad_password_specials = False

            if bad_password_length and bad_password_numbers and bad_password_small_letter and bad_password_big_letter and bad_password_specials:
                bad_password = False
            else:
                self._ask_for_password()

        database.write_db_user(self.name, self.password)
        self.menu()

    def menu(self):
        os.system('cls')

        print("Jestes zalogowany jako ", self.name)
        print("Co chcesz zrobic?")
        print("")
        print("Wylistuj wszystkich użytkowników - opcja 1")
        print("Filtruj użytkowników - opcja 2")
        print("Usuń swojego użytkownika - opcja 3")
        print("Wyloguj - opcja 4")
        opcja = input("")

        if opcja == "1":
            database.find_db_all_users("")

            self._ask_for_enter()

            self.menu()
        elif opcja == "2":
            print("Wpisz tekst dla filtrowania (wielkość liter nie ma znaczenia) ")
            filter_string = input("")
            database.find_db_all_users(filter_string)

            self._ask_for_enter()

            self.menu()
        elif opcja == "3":
            print("Usunąć? ", self.name, " y / n ?")
            delete = input("")

            if delete.upper() == "Y":
                database.delete_db_user(self.name)
                self.name = ""
                self.password = ""
                self.main_menu()
            else:
                self.menu()
        elif opcja == "4":
            self.main_menu()
        else:
            print("Zła opcja")

    def _ask_for_name(self):
        self.name = input("Podaj nazwe uzytkownika: ")

    def _ask_for_enter(self):
        print("Powrót do menu, naciśnij enter ")
        powrot = input("")

    def _ask_for_password(self):
        self.password = getpass.getpass("Podaj haslo: ")
