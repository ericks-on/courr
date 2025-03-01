#!/usr/bin/python3
"""This is the order model"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from models.base_model import Base, Basemodel


class Order(Basemodel, Base):
    """The order model"""
    __tablename__ = 'orders'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    status = Column(String(128), nullable=False, default='pending')
    pickup = Column(String(128), ForeignKey('warehouses.id'), nullable=False)
    delivery = Column(String(128), ForeignKey('warehouses.id'), nullable=False)
    weight = Column(String(128), nullable=False, default='pending')
    dimensions = Column(String(128), nullable=False, default='pending')
    user = relationship('User', backref='orders')
    tracking = relationship('Tracking', back_populates='order')
    delivery_warehouse = relationship('Warehouse', backref='delivery_orders',
                                      foreign_keys=[delivery])
    pickup_warehouse = relationship('Warehouse', backref='pickup_orders',
                                    foreign_keys=[pickup])