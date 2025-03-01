#!/usr/bin/python3
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import Base, Basemodel


class Tracking(Basemodel, Base):
    """The tracking model"""
    __tablename__ = 'tracking'
    order_id = Column(String(60), ForeignKey('orders.id'), nullable=False)
    status = Column(String(128), nullable=False, default='pending') # pending, in transit, delivered
    order = relationship('Order', back_populates='tracking')