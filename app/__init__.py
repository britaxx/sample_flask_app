import os
from flask import Flask
from flask_awscognito import AWSCognitoAuthentication
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    set_access_cookies,
    verify_jwt_in_request_optional,
    get_jwt_identity,
    jwt_required
)
from functools import wraps
from .utils import get_cognito_public_keys
from .config import config_by_name

def create_app(configname):
    app = Flask(__name__)
    
    app.config.from_object(config_by_name[configname])
    
    ## Extensions
    CORS(app)
    # aws_auth = AWSCognitoAuthentication(app)
    jwt = JWTManager(app)
    
    with app.app_context():
        from .my_app import api as api_blueprint
        app.register_blueprint(api_blueprint)
    
        return app