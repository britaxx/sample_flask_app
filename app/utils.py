import json
import os
import requests

def get_cognito_public_keys():
    """ Get jwks Cogniti """
    region = os.environ["AWS_REGION"]
    pool_id = os.environ["AWS_COGNITO_USER_POOL_ID"]
    url = f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/jwks.json"

    resp = requests.get(url)
    print (resp.text)
    return json.dumps(json.loads(resp.text)["keys"][1])



def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS