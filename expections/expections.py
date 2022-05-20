
USER_NOT_FOUND = 1

USER_EXIST = 2

INVALID_USER = 3

INVALID_USER_DATA = 4

class Expection(Exception):
    def __init__(self, code, massage):
        self.code = code
        self.massage = massage

        super().__init__(self.massage)