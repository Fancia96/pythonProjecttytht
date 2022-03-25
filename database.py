import csv
import os
import sys

current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
print(current_dir)
print(os.path.join(current_dir, "db.csv"))
db_path = os.path.join(current_dir, "db.csv")

def check_db_exist(path):
    try:
        os.stat(path)
    except FileNotFoundError:
        f = open(path, "w")
        f.close()

def write_db_user(user, password):
    with open(db_path, 'a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([user, password])

def find_db_user(user, password, check_password):
    with open(db_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if check_password:
                if user.upper() == line[0].upper() and password == line[1]:
                    return True
            else:
                if user.upper() == line[0].upper():
                    return True
        return False

def find_db_all_users(filter_string):

    print("Znalezieni użytkownicy:")

    with open(db_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if filter_string and filter_string.upper() in line[0].upper():
                print(line[0])
            elif not filter_string:
                print(line[0])

def delete_db_user(user):

    array_of_users = []

    with open(db_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if not user.upper() == line[0].upper():
                array_of_users.append(line)

    with open(db_path, 'w+', newline='') as file:
        csv_writer = csv.writer(file)
        for array_line in array_of_users:
            csv_writer.writerow(array_line)

