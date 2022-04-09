import bcrypt


class Room:
    def __init__(self, unique_id: str, password: str):
        self.unique_id = unique_id
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def get_unique_id(self):
        return self.unique_id

    def get_password(self):
        return self.password

    def set_unique_id(self, unique_id):
        self.unique_id = unique_id

    def set_password(self, password):
        self.password = password.encode()
