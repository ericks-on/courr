#!/usr/bin/python3
"""This is the order model"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from models.base_model import Base, Basemodel


class Order(Base, Basemodel):
    """The order model"""
    __tablename__ = 'orders'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    status = Column(String(128), nullable=False, default='pending')
    address = Column(String(128), nullable=False)
    weight = Column(String(128), nullable=False, default='pending')
    dimensions = Column(String(128), nullable=False, default='pending')
    user = relationship('User', back_populates='orders')
    tracking = relationship('Tracking', back_populates='order')