import awsgi
import os
import json
from app import create_app
# from flask import Flask
    
def lambda_handler(event, context):
    print ('Event {}'.format(json.dumps(event)))
    my_app = create_app(os.getenv('APP_ENV') or 'dev')
    return awsgi.response(my_app, event, context)

# We only need this for local development.
if __name__ == '__main__':
    my_app = create_app(os.getenv('APP_ENV') or 'dev')
    my_app.run(host='0.0.0.0')