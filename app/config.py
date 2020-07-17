import os
from jwt.algorithms import RSAAlgorithm
from .utils import  get_cognito_public_keys


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')

    S3_BUCKET =  os.getenv('S3_BUCKET')
    ALLOWED_EXTENSIONS = set(['jpeg', 'png'])
        
    AWS_REGION = os.getenv('AWS_REGION', 'eu-west-1')
    AWS_DEFAULT_REGION = AWS_REGION
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY', None)
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', None)
    AWS_PROFILE = os.getenv('AWS_PROFILE', None)
    
    AWS_COGNITO_DOMAIN =  os.getenv('AWS_COGNITO_DOMAIN')
    AWS_COGNITO_USER_POOL_ID = os.getenv('AWS_COGNITO_USER_POOL_ID')
    AWS_COGNITO_USER_POOL_CLIENT_ID = os.getenv('AWS_COGNITO_USER_POOL_CLIENT_ID')
    AWS_COGNITO_USER_POOL_CLIENT_SECRET =  os.getenv('AWS_COGNITO_USER_POOL_CLIENT_SECRET')
    AWS_COGNITO_REDIRECT_URL = os.getenv('AWS_COGNITO_REDIRECT_URL')

    JWT_PUBLIC_KEY = RSAAlgorithm.from_jwk(get_cognito_public_keys())
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'my_secret_key')
    JWT_PRIVATE_KEY = os.getenv('JWT_PRIVATE_KEY', 'my_secret_key')
    JWT_ALGORITHM = 'RS256'
    JWT_IDENTITY_CLAIM = 'sub'
        
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'
    JWT_REFRESH_COOKIE_PATH = '/'
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_DOMAIN = None
    JWT_SESSION_COOKIE = True
    JWT_COOKIE_SAMESITE = None
    JWT_COOKIE_CSRF_PROTECT = False
        
    JWT_ACCESS_CSRF_HEADER_NAME = 'X-CSRF-TOKEN'
    JWT_ACCESS_CSRF_FIELD_NAME = 'csrf_token'
    
    DYNAMO_TABLE_NAME = os.getenv('DYNAMO_TABLE_NAME')
    
class DevelopmentConfig(Config):
    DEBUG = True
    
config_by_name = dict(
    dev=DevelopmentConfig
)
