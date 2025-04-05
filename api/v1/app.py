#!/usr/bin/python3
"""This is the api file for the v1 version of the api"""
import os
import secrets
from dotenv import load_dotenv
from datetime import timedelta, datetime, timezone
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flasgger import Swagger
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import create_access_token, JWTManager
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from flask_jwt_extended import set_access_cookies
from passlib.hash import bcrypt
from models.user import User
from werkzeug.exceptions import BadRequest
from models import storage
from api.v1.endpoints import app_views
from .mpesa import MpesaClient 
from .mpesa import MpesaPaymentError, MpesaStatusError
import logging
import base64
import json
import logging
import uuid
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('mpesa_flask_logger')


load_dotenv()

mpesa_client = MpesaClient()

app = Flask(__name__)
mail = Mail(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app, resources={r"*": {
    "origins": ["http://localhost:3000"],
    "allow_headers": ["Content-Type", "Authorization"],
    "supports_credentials": True,
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
}})

# @app.after_request
# def after_request(response):
#     response.headers.add("Access-Control-Allow-Credentials", "true")
#     return response

# jwt access token config
app.config["JWT_TOKEN_LOCATION"] = ["headers","cookies"]
app.config["JWT_ACCESS_COOKIE_NAME"] = "accessToken"

# email config
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config['MAIL_DEBUG'] = True
mail=Mail(app)


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
# app.config["JWT_COOKIE_SECURE"] = True
secret_key = os.environ.get('SECRET_KEY')
jwt_key = os.environ.get('JWT_KEY')
app.config['SECRET_KEY'] = secret_key
# app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_SECRET_KEY'] = jwt_key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.register_blueprint(app_views)

app.url_map.strict_slashes = False

@app.route('/pay', methods=['POST'])
def pay():
    """Triggers an STK push for payment."""
    try:
        data = request.json
        phone_number = data.get('phoneNumber')
        amount = float(data.get('amount', 0))
        reference = data.get('reference', str(uuid.uuid4()))
        
        if not phone_number:
            return jsonify({'success': False, 'error': 'Phone number is required'}), 400
            
        result = mpesa_client.initiate_stk_push(phone_number, amount, reference)
        return jsonify(result)
    
    except MpesaPaymentError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    
    except Exception as e:
        logger.error(f"Unexpected error in STK push: {e}")
        return jsonify({'success': False, 'error': 'An unexpected error occurred'}), 500



@app.route('/api/mpesa/status', methods=['POST'])
def query_status():
    try:
        data = request.json
        transaction_id = data.get('transaction_id')
        identifier_type = data.get('identifier_type', '1')
        
        if not transaction_id:
            return jsonify({'success': False, 'error': 'Transaction ID is required'}), 400
            
        result = mpesa_client.query_transaction_status(transaction_id, identifier_type)
        return jsonify(result)
    
    except MpesaStatusError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    
    except Exception as e:
        logger.error(f"Unexpected error in status query: {e}")
        return jsonify({'success': False, 'error': 'An unexpected error occurred'}), 500



# route for M-Pesa responses
@app.route('/api/mpesa/callback', methods=['POST'])
def mpesa_callback():
    try:
        # Process callback data
        callback_data = request.json
        logger.info(f"M-Pesa callback received: {callback_data}")
        
        #  add some logic for how to handle the callback data.....eg saving it to the database
        #  can also check the status of the transaction here
        # and update the database accordingly
        
        return jsonify({'ResultCode': 0, 'ResultDesc': 'Accepted'})
    
    except Exception as e:
        logger.error(f"Error processing callback: {e}")
        return jsonify({'ResultCode': 1, 'ResultDesc': 'Rejected'}), 500


    
    
@app.route('/email_test', methods=['GET'])
def email_test():
    """sends a test email"""
    try:
        msg = Message('Test Email', sender = 'erickson.mbuvi@nebulaanalytics.org',
                      recipients=['mutisyaerickson@gmail.com'])
        msg.body = "This is a test email"
        with mail.connect() as conn:
            conn.send(msg)
            return jsonify({"msg": "Email sent"}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Email not sent"}), 400

@app.route('/api/v1/token/auth', methods=['POST'])
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
                           refresh_token=refresh_token,
                           user_type=user.user_type), 200
        return jsonify({"msg": "Wrong Username or Password"}), 401
    return jsonify({"msg": "Wrong Username or Password"}), 401

@app.route('/api/v1/token/verify', methods=['GET'])
@jwt_required()
def confirm():
    """confirms the user's access token from headers"""
    try:
        access_token = request.headers.get('Authorization').split(" ")[1]
    except:
        # check from cookie if no headers
        access_token = request.cookies.get("accessToken")

    if not access_token:
        return jsonify({"msg": "Missing access token"}), 400
    try:
        username = get_jwt_identity()
        user = storage.get_user(username)
        return jsonify({"msg": "Valid access token", "user": user.to_dict()}), 200
    except:
        print("Invalid access token")
        return jsonify({"msg": "Invalid access token"}), 401

@app.route('/api/v1/token/refresh', methods=['GET'])
@jwt_required()
def refresh():
    """refreshes access token"""
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token), 200

@app.route('/api/v1/auth/logout', methods=['GET'])
@jwt_required()
def logout():
    """logs out user"""
    response = make_response(jsonify({"msg": "Successfully logged out"}))
    response.set_cookie("accessToken", "", expires=0, httponly=True)
    return response

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
    host = os.environ.get('API_HOST')
    if not host:
        host = '0.0.0.0'
    port = os.environ.get('API_PORT')
    if not port:
        port = 5000
    app.run(host=host, port = port, debug=True)