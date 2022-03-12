import getpass
import os
import csv

os.system('cls')

print("Zarejestruj się")
print(getpass.getuser())
name = input("podaj nazwe uzytkownika")


password = getpass.getpass("podaj haslo")

print(name)
print(password)

#
# password = getpass.getpass("prompt = 'Enter password")
# print(password)

# with open('db.csv', newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for row in spamreader:
#         print(', '.join(row))
