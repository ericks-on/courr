#!/usr/bin/python3
"""Contains all the endpoints for the users"""
from flask import Blueprint, jsonify, abort, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flasgger.utils import swag_from
from models import storage
from models.user import User


user_bp = Blueprint('users', __name__, url_prefix='/users')


@user_bp.route('/', methods=['GET'])
@jwt_required()
@swag_from('documentation/user/all_users.yml', methods=['GET'])
def all_users():
    """To obtain all users"""
    request_user = storage.get_user(get_jwt_identity())
    if request_user.user_type != 'admin':
        return jsonify({"users": request_user.to_dict()}), 200
    users = [user.to_dict() for user in storage.all(User)]
    return jsonify({"users": users}), 200

@user_bp.route('/', methods=['POST'])
@jwt_required()
@swag_from('documentation/user/add_user.yml', methods=['POST'])
def add_user():
    """ Adds new user"""
    request_user = storage.get_user(get_jwt_identity())
    if request_user.user_type != 'admin':
        abort(403)
    if not request.json():
        abort(400, "Not a JSON")
    if not request.json().get("username"):
        abort(400, "Missing username")
    if not request.json().get("password"):
        abort(400, "Missing password")
    username = request.json().get("username")
    password = request.json().get("password")
    user_type = request.json().get("user_type")
    if not user_type:
        user_type = "normal"
    email = request.json().get("email")
    first_name = request.json().get("first_name")
    last_name = request.json().get("last_name")
    new_user = User(username=username, password=password, user_type=user_type,
                    email=email, first_name=first_name,
                    last_name=last_name)
    storage.add(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201

@user_bp.route('/self', methods=['GET'])
@jwt_required()
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_user():
    """ Gets user information"""
    request_user = storage.get_user(get_jwt_identity())
    if not request_user:
        abort(404)
    return jsonify({"user": request_user.to_dict()}), 200

@user_bp.route('/<user_id>', methods=['DELETE'])
@jwt_required()
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user():
    """Deleting a user"""
    user = storage.get_user(get_jwt_identity())
    if not user:
        abort(404)
        
    if user.user_type != 'admin':
        abort(403)
    del_user = storage.get(User, user_id)
    if not del_user:
        abort(404)
    storage.delete(del_user)
    storage.save()
    return jsonify({}), 200