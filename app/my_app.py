
import os, json
import boto3
import uuid
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_awscognito import AWSCognitoAuthentication
from flask import Blueprint, current_app
from flask_jwt_extended import (
    JWTManager,
    set_access_cookies,
    verify_jwt_in_request_optional,
    get_jwt_identity,
    jwt_required,
    get_current_user,
    get_jwt_claims,
    get_raw_jwt
)
from .tools import get_photos, upload_file_to_s3
from .forms import PhotoForm
from .utils import allowed_file


api = Blueprint('prod', __name__)
aws_auth = AWSCognitoAuthentication(current_app)

@api.route('/')
def index():
    return render_template("index.html")

@api.route('/sign_in')
def sign_in():
    return redirect(aws_auth.get_sign_in_url())

@api.route("/loggedin", methods=["GET"])
def logged_in():
    access_token = aws_auth.get_access_token(request.args)
    # print (access_token)
    resp = make_response(redirect(url_for("prod.protected")))
    # print(url_for("prod.protected"))
    # print("Application root {}, Server_NAME {}".format(current_app.config['APPLICATION_ROOT'], current_app.config['SERVER_NAME']))
    print (json.dumps(access_token))
    set_access_cookies(resp, access_token, max_age=30 * 60)
    return resp


@api.route("/app", methods=['GET', 'POST'])
def protected():
    verify_jwt_in_request_optional()
    if get_jwt_identity():
        raw_jwt = get_raw_jwt()
        # print ("raw_jwt {}".format(json.dumps(raw_jwt)))
        ## Upload New Images
        form = PhotoForm()
        if form.validate_on_submit():
            # note for futur to transform .gif into .mov or mp4
            file =  form.photo.data
            if allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
                output = upload_file_to_s3(file, current_app.config["S3_BUCKET"])
            else:
                form.photo.errors.append('File is not supported, only {}'.format(current_app.config['ALLOWED_EXTENSIONS']))
        ## Get photos
        photos = get_photos(current_app.config['S3_BUCKET'])
        # print ("Photos {}".format(json.dumps(photos)))
        return render_template("protected.html", user=raw_jwt['username'], photos=photos, form=form)
    else:
        return redirect(aws_auth.get_sign_in_url())


# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         # if user is not logged in, redirect to login page      
#         if not request.headers["authorization"]:
#             return redirect("login page")
#         # get user via some ORM system
#         user = User.get(request.headers["authorization"])
#         # make user available down the pipeline via flask.g
#         g.user = user
#         # finally call f. f() now haves access to g.user
#         return f(*args, **kwargs)
   
#     return wrap

# @api.route("/secret")
# @jwt_required
# def protected():
#     return "Secret Info", 200