import bcrypt


class Room:
    def __init__(self, owner_id, unique_id: str, password: str):
        self.id = None
        self.owner_id = owner_id
        self.unique_id = unique_id
        self.password = password
        self.subject = ""
        self.points = 0

    def get_unique_id(self):
        return self.unique_id

    def get_password(self):
        return self.password

    def set_unique_id(self, unique_id):
        self.unique_id = unique_id

    def set_password(self, password):
        self.password = password.encode()

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_owner_id(self):
        return self.owner_id

    def set_owner_id(self, owner_id):
        self.owner_id = owner_id