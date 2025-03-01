#!/usr/bin/python3
"""Contains the endpoints for the warehouses"""
from flask import Blueprint, request, jsonify, abort
from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import storage
from models.warehouse import Warehouse


warehouses_bp = Blueprint('warehouses', __name__, url_prefix='/warehouses')


@warehouses_bp.route('/', methods=['GET'])
@jwt_required()
@swag_from('documentation/warehouse/all_warehouses.yml', methods=['GET'])
def all_warehouses():
    """To obtain all warehouses"""
    # obtain current user
    username = get_jwt_identity()
    # get user from storage
    request_user = storage.get_user(username)

    # if user is not found, return 401
    if not request_user:
        abort(401)


    warehouses = [warehouse.to_dict() for warehouse in storage.all(Warehouse)]

    return jsonify({"warehouses": warehouses}), 200