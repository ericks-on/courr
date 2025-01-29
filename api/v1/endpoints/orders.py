#!/usr/bin/python3
"""Contains the endpoints for the orders"""
from flask import Blueprint, request, jsonify, abort
from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import storage
from models.order import Order
from models.tracking import Tracking


orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('/', methods=['GET'])
@jwt_required()
def all_orders():
    """To obtain all orders"""
    # obtain current user
    username = get_jwt_identity()
    # get user from storage
    request_user = storage.get_user(username)

    # if user is not found, return 404
    if not request_user:
        abort(404)
    
    # if user is not admin, return only the user's orders
    if request_user.user_type != 'admin':
        orders = [order.to_dict() for order in storage.all(Order)
                  if order.user_id == request_user.id]
    
    # if user is admin, return all orders
    else:
        orders = [order.to_dict() for order in storage.all(Order)]
    
    return jsonify({"orders": orders}), 200

@orders_bp.route('/', methods=['POST'])
@jwt_required()
def add_order():
    """ Adds new order"""
    # obtain current user
    username = get_jwt_identity()
    # get user from storage
    request_user = storage.get_user(username)

    # if user is not found, return 404
    if not request_user:
        abort(403)

    # if not a JSON, return 400
    if not request.json():
        abort(400)

    # obtain the fields 
    delivery_address = request.json.get('address')
    warehouse_id = request.json.get('warehouse_id')

    if not delivery_address or not warehouse_id:
        abort(400)

    # create the order
    new_order = Order(user_id=request_user.id, address=delivery_address)
    storage.new(new_order)
    storage.save()

    # create the tracking
    new_tracking = Tracking(order_id=new_order.id, warehouse_id=warehouse_id)
    storage.new(new_tracking)
    storage.save()

    return jsonify(new_order.to_dict()), 201

@orders_bp.route('/<order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """To obtain an order"""
    # obtain current user
    username = get_jwt_identity()
    # get user from storage
    request_user = storage.get_user(username)

    # if user is not found, return 404
    if not request_user:
        abort(404)

    # get the order
    order = storage.get(Order, order_id)

    # if order is not found, return 404
    if not order:
        abort(404)

    # if user is not admin and order does not belong to user, return 403
    if request_user.user_type != 'admin' and order.user_id != request_user.id:
        abort(403)

    return jsonify(order.to_dict()), 200

@orders_bp.route('/<order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    """To delete an order"""
    # obtain current user
    username = get_jwt_identity()
    # get user from storage
    request_user = storage.get_user(username)

    # if user is not found, return 404
    if not request_user:
        abort(403)

    # get the order
    order = storage.get(Order, order_id)

    # if order is not found, return 404
    if not order:
        abort(404)

    # if user is not admin and order does not belong to user, return 403
    if request_user.user_type != 'admin' and order.user_id != request_user.id:
        abort(403)

    storage.delete(order)
    storage.save()

    return jsonify({}), 200

@orders_bp.route('/<order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    """To update an order"""
    # obtain current user
    username = get_jwt_identity()
    # get user from storage
    request_user = storage.get_user(username)

    # if user is not found, return 404
    if not request_user:
        abort(403)

    # get the order
    order = storage.get(Order, order_id)

    # if order is not found, return 404
    if not order:
        abort(404)

    # if user is not admin and order does not belong to user, return 403
    if request_user.user_type != 'admin' and order.user_id != request_user.id:
        abort(403)

    # if not a JSON, return 400
    if not request.json():
        abort(400)

    # obtain the fields 
    delivery_address = request.json.get('address')
    warehouse_id = request.json.get('warehouse_id')
    weight = request.json.get('weight')
    dimensions = request.json.get('dimensions')

    if not delivery_address or not warehouse_id or not weight or not dimensions:
        abort(400)

    order.address = delivery_address
    order.weight = weight
    order.dimensions = dimensions
    storage.save()

    return jsonify(order.to_dict()), 200

@orders_bp.route('/<order_id>/tracking', methods=['GET'])
@jwt_required()
def get_order_tracking(order_id):
    """To obtain the tracking of an order"""
    # obtain current user
    username = get_jwt_identity()
    # get user from storage
    request_user = storage.get_user(username)

    # if user is not found, return 404
    if not request_user:
        abort(404)

    # get the order
    order = storage.get(Order, order_id)

    # if order is not found, return 404
    if not order:
        abort(404)

    # if user is not admin and order does not belong to user, return 403
    if request_user.user_type != 'admin' and order.user_id != request_user.id:
        abort(403)

    # get the tracking
    tracking = storage.get(Tracking, order.tracking_id)

    return jsonify(tracking.to_dict()), 200

@orders_bp.route('/<order_id>/tracking', methods=['PUT'])
@jwt_required()
def update_order_tracking(order_id):
    """To update the tracking of an order"""
    # obtain current user
    username = get_jwt_identity()
    # get user from storage
    request_user = storage.get_user(username)

    # if user is not found, return 404
    if not request_user:
        abort(404)

    # get the order
    order = storage.get(Order, order_id)

    # if order is not found, return 404
    if not order:
        abort(404)

    # if user is not admin and order does not belong to user, return 403
    if request_user.user_type != 'admin' and order.user_id != request_user.id:
        abort(403)

    # if not a JSON, return 400
    if not request.json():
        abort(400)

    # obtain the fields 
    status = request.json.get('status')

    if not status:
        abort(400)

    # get the tracking
    tracking = storage.get(Tracking, order.tracking_id)
    tracking.status = status
    storage.save()

    return jsonify(tracking.to_dict()), 200

@orders_bp.route('/<order_id>/tracking', methods=['POST'])
@jwt_required()
def add_order_tracking(order_id):
    """To add the tracking of an order"""
    # obtain current user
    username = get_jwt_identity()
    # get user from storage
    request_user = storage.get_user(username)

    # if user is not found, return 404
    if not request_user:
        abort(404)

    # get the order
    order = storage.get(Order, order_id)

    # if order is not found, return 404
    if not order:
        abort(404)

    # if user is not admin and order does not belong to user, return 403
    if request_user.user_type != 'admin' and order.user_id != request_user.id:
        abort(403)

    # if not a JSON, return 400
    if not request.json():
        abort(400)

    # obtain the fields 
    status = request.json.get('status')
    warehouse_id = request.json.get('warehouse_id')

    if not status or not warehouse_id:
        abort(400)

    # create the tracking
    new_tracking = Tracking(order_id=order.id, status=status)
    storage.new(new_tracking)
    storage.save()

    return jsonify(new_tracking.to_dict()), 201
