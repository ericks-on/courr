#!/usr/bin/python3
from flask import Blueprint
from api.v1.endpoints.users import user_bp


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# registering other blueprints
app_views.register_blueprint(user_bp)