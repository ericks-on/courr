#!/usr/bin/python3
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import Base, Basemodel


class Tracking(Base, Basemodel):
    """The tracking model"""
    __tablename__ = 'tracking'
    order_id = Column(String(60), ForeignKey('orders.id'), nullable=False)
    warehouse_id = Column(String(60), ForeignKey('warehouses.id'), nullable=True)
    status = Column(String(128), nullable=False, default='pending') # pending, in transit, delivered
    order = relationship('Order', back_populates='tracking')
    warehouse = relationship('Warehouse', back_populates='tracking')