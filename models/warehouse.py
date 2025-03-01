#!/usr/bin/python3
"""This is the warehouse model"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from models.base_model import Base, Basemodel


class Warehouse(Basemodel, Base):
    """The warehouse model"""
    __tablename__ = 'warehouses'
    name = Column(String(128), nullable=False)
    country = Column(String(128), nullable=False)
    county = Column(String(128), nullable=False)
    town = Column(String(128), nullable=False)