import getpass
import json
import os
from abc import ABC

from starlette.authentication import SimpleUser


class User(SimpleUser, ABC):
    def __init__(self, name, password):
        super().__init__(name)
        self.id = None
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

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def toJSON(self):
        #return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        return {"id": self.id, "name": self.name}
