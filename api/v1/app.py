#!/usr/bin/python3
"""This is the api file for the v1 version of the api"""
import os
import secrets
from dotenv import load_dotenv
from datetime import timedelta, datetime, timezone
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flasgger import Swagger
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import create_access_token, JWTManager
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from flask_jwt_extended import set_access_cookies
from passlib.hash import bcrypt
from models.user import User
from werkzeug.exceptions import BadRequest
from models import storage
from api.v1.endpoints import app_views


load_dotenv()


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.teardown_appcontext
def teardown(exception=None):
    """calls storage close method to remove current session"""
    storage.close()

@app.errorhandler(404)
def not_found_error(error):
    """defines what happens if code 404 is raised"""
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.errorhandler(400)
def bad_request_error(error):
    """defines what happens if code 400 is raised"""
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(401)
def unauthorized_error(error):
    """defines what happens if code 401 is raised"""
    return make_response(jsonify({'error': 'Unauthorized'}), 401)

@app.errorhandler(403)
def forbidden_error(error):
    """defines what happens if code 403 is raised"""
    return make_response(jsonify({'error': 'Forbidden'}), 403)

@app.errorhandler(405)
def method_not_allowed_error(error):
    """defines what happens if code 405 is raised"""
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)

# Documentation by swagger
app.config['SWAGGER'] = {
        'title': 'Courrier RESTFull API'
        }
Swagger(app)

jwt = JWTManager(app)
csrf = CSRFProtect(app)
app.config["JWT_COOKIE_SECURE"] = True #remember to change to True
secret_key = os.environ.get('SECRET_KEY')
jwt_key = os.environ.get('JWT_KEY')
app.config['SECRET_KEY'] = secret_key
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_SECRET_KEY'] = jwt_key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.register_blueprint(app_views)



@app.route('/api/v1/token/auth', methods=['POST'])
@csrf.exempt
def login():
    """authenticates user and creates an access token"""
    all_users = storage.all(User)
    all_usernames = [user.username for user in all_users]
    username = request.get_json().get("username")
    password = request.get_json().get("password")
    if not username or not password:
        return jsonify({"msg": "Missing username parameter"}), 400

    if username in all_usernames:
        user = storage.get_user(username)
        hashed_pwd = user.password
        if bcrypt.verify(password, hashed_pwd) == True:
            access_token = create_access_token(identity=username, fresh=True)
            refresh_token = create_access_token(identity=username)
            return jsonify(access_token=access_token,
                           refresh_token=refresh_token), 200
        return jsonify({"msg": "Wrong Username or Password"}), 401
    return jsonify({"msg": "Wrong Username or Password"}), 401
    
@app.route('/api/v1/token/refresh', methods=['GET'])
@jwt_required()
def refresh():
    """refreshes access token"""
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token), 200

@app.after_request
def refresh_expiring_jwts(response):
    """refreshes access token if it is about to expire"""
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response



if __name__ == "__main__":
    # # Creating users
    # admin_user = User(
    #     first_name="Admin",
    #     last_name="User",
    #     email="admin@example.com",
    #     password="pass123",  # Replace with a securely hashed password
    #     username="admin_user",
    #     user_type="admin",
    #     address="123 Admin St"
    # )

    # normal_user = User(
    #     first_name="John",
    #     last_name="Doe",
    #     email="john.doe@example.com",
    #     password="pass123",
    #     username="john_doe",
    #     user_type="normal",
    #     address="456 Normal Ave"
    # )

    # storage.add(admin_user)
    # storage.add(normal_user)
    # storage.save()

    host = os.environ.get('API_HOST')
    if not host:
        host = '0.0.0.0'
    port = os.environ.get('API_PORT')
    if not port:
        port = 5000
    app.run(host=host, port = port, debug=True)