#!/usr/bin/python3
"""This contains the base model for all the other models"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from passlib.hash import bcrypt


Base = declarative_base()
time_format = "%Y-%m-%dT%H:%M:%S.%f"


class Basemodel:
    """This is the base model for all the othe models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        """initialization"""
        if kwargs:
            for k, v in kwargs.items():
                if k == "password":
                    v = bcrypt.hash(v)
                setattr(self, k, v)

        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.utcnow()
        if not self.updated_at:
            self.updated_at = self.created_at

    def __str__(self):
        """The string representation"""
        return "[{}].({}): {}".format(self.__class__.__name__, self.id,
                                      self.to_dict())

    def to_dict(self):
        """creates a json serializable dict containing all attributes"""
        temp_dict = self.__dict__
        my_dict = {}
        for k, v in temp_dict.items():
            if k == "created_at":
                my_dict["created_at"] = temp_dict["created_at"].strftime(time_format)
            elif k == "updated_at":
                my_dict["updated_at"] = temp_dict["updated_at"].strftime(time_format)
            if k == "password" or k == '_sa_instance_state':
                pass
            else:
                my_dict[k] = v
        return my_dict
