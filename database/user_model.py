import getpass
import os

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password
    def get_name(self):
        return self.name
    def get_password(self):
        return self.password
    def set_name(self, name):
        self.name = name
    def set_password(self, password):
        self.password = password

