#!/usr/bin/python3
from sqlalchemy import Column, String, DateTime
from models.base_model import Base, Basemodel


class User(Base, Basemodel):
    """This is the user model"""
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    username = Column(String(128), nullable=False)