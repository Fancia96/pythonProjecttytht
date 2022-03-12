# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
import getpass

# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
import os
import sys

def check_db_exist(path):
    try:
        os.stat(path)
    except FileNotFoundError:
        f = open(path, "w")
        f.close()

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    print(current_dir)
    print(os.path.join(current_dir, "db.csv"))
    db_path = os.path.join(current_dir, "db.csv")
    check_db_exist(db_path)
#     print_hi('PyCharm')

    with open(db_path, 'a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['user 1', 'haslo 1'])

    with open(db_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            print(line)

    print("Witam")
    print("Zaloguj - opcja 1")
    print("Zarejestruj - opcja 2")
    opcja = input("")



    if opcja == 1:
        pass
    else:
        import register

        #register.name

        pass





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
