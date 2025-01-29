#!/usr/bin/python3
"""This is the warehouse model"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from models.base_model import Base, Basemodel


class Warehouse(Base, Basemodel):
    """The warehouse model"""
    __tablename__ = 'warehouses'
    name = Column(String(128), nullable=False)
    location = Column(String(128), nullable=False)