#here we are creating models for the base
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class users(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True, index=True)
    email = Column(String, unique=True)# to have a unique emails
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key = True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(String)
    complete = Column(Boolean, default = False)
    owner_id = Column(Integer, ForeignKey('users.id'))

