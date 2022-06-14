from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from starlette.authentication import SimpleUser

from database.database import Base
from database.room_model import room_user_table


class User(Base, SimpleUser):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    rooms = relationship('Room', secondary=room_user_table, back_populates="users")

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
