from sqlalchemy import Column, Integer, String, ForeignKey, Table, Numeric
from sqlalchemy.orm import relationship

from database.database import Base

room_user_table = Table(
    'room_user',
    Base.metadata,
    Column('room_id', ForeignKey('room.id'), primary_key=True),
    Column('user_id', ForeignKey('user.id'), primary_key=True)
)

class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    password = Column(String)
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship('User')
    topic = Column(String)
    votes = relationship('RoomVote', back_populates='room')
    users = relationship('User', secondary=room_user_table, back_populates="rooms", lazy="dynamic")

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

    def get_subject(self):
        return self.subject

    def set_subject(self, subject):
        self.subject = subject

    #def get_points(self):
    #    return self.points

    #def set_points(self, points):
    #    self.points = points


class RoomVote(Base):
    __tablename__ = 'room_vote'
    id = Column(Integer, primary_key=True, autoincrement=True)

    room_id = Column(Integer, ForeignKey('room.id'))
    room = relationship('Room', back_populates="votes")

    user = relationship('User')
    user_id = Column(Integer, ForeignKey('user.id'))
    
    vote = Column(Numeric)
