#!/usr/bin/python3
from sqlalchemy import Column, String, DateTime
from models.base_model import Base, Basemodel


class User(Basemodel, Base):
    """This is the user model"""
    __tablename__ = 'users'
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    username = Column(String(128), nullable=False)
    user_type = Column(String(128), nullable=False, default='normal')