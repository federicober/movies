from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__: str = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, index=True, unique=True)
    password = Column(String)
