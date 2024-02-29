from flask import Flask, request, redirect, session, jsonify
import requests
import json
import os
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = Flask(__name__)
# You must configure these 3 values from Facebook
app.secret_key = "your-secret-key"
FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET')

@app.route("/")
def index():
    return """
        <a href="/login">Login with Facebook</a>
    """

@app.route("/login")
def login():
    facebook_auth_url = "https://www.facebook.com/v19.0/dialog/oauth?"
    params = {
        "client_id": FACEBOOK_APP_ID,
        "redirect_uri": "http://localhost:5678/authorize",  # replace with your web server url
        "state": "st=state123abc,ds=123456789",  # optional
        "scope": "public_profile,email",  # optional
    }
    return redirect(facebook_auth_url + requests.compat.urlencode(params))

@app.route("/authorize")
def authorize():
    code = request.args.get("code")
    params = {
        "client_id": FACEBOOK_APP_ID,
        "redirect_uri": "http://localhost:5678/authorize",  # replace with your web server url
        "client_secret": FACEBOOK_APP_SECRET,
        "code": code
    }
    response = requests.get("https://graph.facebook.com/v12.0/oauth/access_token",
                            params=params)
    log.info(f"Response from token endpoint {response.text}")
    response_dict = json.loads(response.text)

    if 'access_token' in response_dict:
        session['access_token'] = response_dict['access_token']
        # Use the access token to fetch user's name and id
        user_info_params = {
            "fields": "id,name, picture",
            "access_token": session['access_token']
        }
        user_info_response = requests.get("https://graph.facebook.com/me", params=user_info_params)
        log.info(f"Response from ME endpoint {user_info_response.text}")

        user_info = json.loads(user_info_response.text)
        return f"<img href='{user_info['picture']['data']['url']}' /><h1>Hello {user_info['name']}</h1>"
    else:
        return "Failed to log in!"

if __name__ == "__main__":
    app.run(debug=True, port=5678, host="localhost")