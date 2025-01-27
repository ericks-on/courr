#!/usr/bin/python3
"""This is the init file for the models package"""
from models.engine.db_storage import DBStorage


storage = DBStorage()
storage.reload()