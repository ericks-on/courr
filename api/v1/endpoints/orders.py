#!/usr/bin/python3
"""Contains the endpoints for the orders"""
from flask import Blueprint, request, jsonify, abort, make_response, current_app
from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models import storage
from models.order import Order
from models.tracking import Tracking
from models.warehouse import Warehouse


orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/', methods=['OPTIONS'], strict_slashes=False)
def options():
    """To handle the preflight request"""
    response = make_response(jsonify({}))
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response, 204

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
    """ Adds new order and sends notification email to the user"""
    from api.v1.endpoints.utils.orders import send_order_notification_email


    mail = current_app.extensions['mail']

    # obtain current user
    username = get_jwt_identity()
    # get user from storage
    request_user = storage.get_user(username)

    # if user is not found, return 404
    if not request_user:
        abort(403)

    # if not a JSON, return 400
    if not request.get_json():
        abort(400)

    # obtain the fields
    delivery_warehouse = request.get_json().get('delivery_warehouse')
    pickup_warehouse = request.get_json().get('pickup_warehouse')

    if not delivery_warehouse or not pickup_warehouse:
        abort(400)

    # create the order
    new_order = Order(user_id=request_user.id, pickup=pickup_warehouse,
                      delivery=delivery_warehouse)
    storage.add(new_order)
    storage.save()

    # create the tracking
    new_tracking = Tracking(order_id=new_order.id)
    storage.add(new_tracking)
    storage.save()

    # get warehouse names
    pickup_warehouse_name = storage.get(Warehouse, pickup_warehouse).name
    delivery_warehouse_name = storage.get(Warehouse, delivery_warehouse).name


    # Send notification email to the user
    send_order_notification_email(mail, request_user.email, new_order, pickup_warehouse_name,
                                  delivery_warehouse_name)

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
    """Update an order, create tracking record, and notify the user."""
    from api.v1.endpoints.utils.orders import send_order_update_notification

    mail = current_app.extensions['mail']
    # Obtain current user
    username = get_jwt_identity()
    # Get user from storage
    request_user = storage.get_user(username)

    # If user is not found, return 404
    if not request_user:
        abort(404)
    
    # Only admin can update orders
    if request_user.user_type != 'admin':
        abort(403, description="Only admin can update orders")
    
    # Get the order
    order = storage.get(Order, order_id)
    if not order:
        abort(404, description="Order not found")
    
    # Get request data
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    
    # Fields that can be updated
    allowed_fields = ['status', 'weight', 'dimensions']
    
    # Track changes for notification
    changes = {}
    for key, value in data.items():
        if key in allowed_fields:
            setattr(order, key, value)
            changes[key] = value
    
    # Create a new tracking record with the updated status
    if 'status' in data:
        tracking = Tracking(order_id=order_id, status=data['status'])
        storage.add(tracking)
    
    # Save changes
    storage.save()
    
    # Send notification email if there are changes
    if changes:
        send_order_update_notification(mail, order.user.email, order, changes)
    order = order.to_dict()
    order['user'] = order['user'].to_dict()
    return jsonify(order), 200


@orders_bp.route('/<order_id>/tracking', methods=['GET'])
@jwt_required()
def get_order_tracking(order_id):
    """Get all tracking records for a specific order"""
    # Obtain current user
    username = get_jwt_identity()
    # Get user from storage
    request_user = storage.get_user(username)

    # If user is not found, return 404
    if not request_user:
        abort(404)
    
    # Get the order
    order = storage.get(Order, order_id)
    if not order:
        abort(404, description="Order not found")
    
    # Check if user is authorized to view this order's tracking
    if request_user.user_type != 'admin' and order.user_id != request_user.id:
        abort(403, description="Not authorized to view this order's tracking")
    
    # Get all tracking records for this order, sorted by creation date
    tracking_history = sorted(
        [tracking.to_dict() for tracking in order.tracking],
        key=lambda x: x['created_at']
    )
    
    return jsonify({"tracking_history": tracking_history}), 200

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
    if not request.get_json():
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
    if not request.get_json():
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

@orders_bp.route('/<order_id>/tracking', methods=['GET'])
@jwt_required()
def get_tracking_history(order_id):
    """Get tracking history for a specific order"""
    # Obtain current user
    username = get_jwt_identity()
    # Get user from storage
    request_user = storage.get_user(username)

    # If user is not found, return 404
    if not request_user:
        abort(404)
    
    # Get the order
    order = storage.get(Order, order_id)
    if not order:
        abort(404, description="Order not found")
    
    # Check if user is authorized to view this order's tracking
    if request_user.user_type != 'admin' and order.user_id != request_user.id:
        abort(403, description="Not authorized to view this order's tracking")
    
    # Get all tracking records for this order
    tracking_history = [tracking.to_dict() for tracking in order.tracking]
    
    return jsonify({"tracking_history": tracking_history}), 200


@orders_bp.route('/<order_id>/tracking', methods=['POST'])
@jwt_required()
def create_tracking(order_id):
    """Create a new tracking record for an order"""
    # Obtain current user
    username = get_jwt_identity()
    # Get user from storage
    request_user = storage.get_user(username)

    # If user is not found, return 404
    if not request_user:
        abort(404)
    
    # Only admin can create tracking records
    if request_user.user_type != 'admin':
        abort(403, description="Only admin can create tracking records")
    
    # Get the order
    order = storage.get(Order, order_id)
    if not order:
        abort(404, description="Order not found")
    
    # Get request data
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    
    # Validate status
    status = data.get('status')
    if not status:
        abort(400, description="Status is required")
    
    # Create new tracking record
    tracking = Tracking(order_id=order_id, status=status)
    
    # Update order status
    order.status = status
    
    # Save to storage
    storage.new(tracking)
    storage.save()
    
    return jsonify(tracking.to_dict()), 201


@orders_bp.route('/tracking/<tracking_id>', methods=['GET'])
@jwt_required()
def get_tracking(tracking_id):
    """Get a specific tracking record"""
    # Obtain current user
    username = get_jwt_identity()
    # Get user from storage
    request_user = storage.get_user(username)

    # If user is not found, return 404
    if not request_user:
        abort(404)
    
    # Get the tracking record
    tracking = storage.get(Tracking, tracking_id)
    if not tracking:
        abort(404, description="Tracking record not found")
    
    # Get the order associated with this tracking
    order = tracking.order
    
    # Check if user is authorized to view this tracking
    if request_user.user_type != 'admin' and order.user_id != request_user.id:
        abort(403, description="Not authorized to view this tracking")
    
    return jsonify(tracking.to_dict()), 200


@orders_bp.route('/tracking/<tracking_id>', methods=['PUT'])
@jwt_required()
def update_tracking(tracking_id):
    """Update a tracking record"""
    # Obtain current user
    username = get_jwt_identity()
    # Get user from storage
    request_user = storage.get_user(username)

    # If user is not found, return 404
    if not request_user:
        abort(404)
    
    # Only admin can update tracking records
    if request_user.user_type != 'admin':
        abort(403, description="Only admin can update tracking records")
    
    # Get the tracking record
    tracking = storage.get(Tracking, tracking_id)
    if not tracking:
        abort(404, description="Tracking record not found")
    
    # Get request data
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    
    # Update status if provided
    if 'status' in data:
        tracking.status = data['status']
        # Update the order's status as well
        tracking.order.status = data['status']
    
    # Save changes
    storage.save()
    
    return jsonify(tracking.to_dict()), 200


@orders_bp.route('/tracking/<tracking_id>', methods=['DELETE'])
@jwt_required()
def delete_tracking(tracking_id):
    """Delete a tracking record"""
    # Obtain current user
    username = get_jwt_identity()
    # Get user from storage
    request_user = storage.get_user(username)

    # If user is not found, return 404
    if not request_user:
        abort(404)
    
    # Only admin can delete tracking records
    if request_user.user_type != 'admin':
        abort(403, description="Only admin can delete tracking records")
    
    # Get the tracking record
    tracking = storage.get(Tracking, tracking_id)
    if not tracking:
        abort(404, description="Tracking record not found")
    
    # Delete the tracking record
    storage.delete(tracking)
    storage.save()
    
    return jsonify({}), 204
