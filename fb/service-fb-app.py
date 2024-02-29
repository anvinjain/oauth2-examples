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
    params = {
        "client_id": FACEBOOK_APP_ID,
        "client_secret": FACEBOOK_APP_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.get("https://graph.facebook.com/oauth/access_token", params=params)
    log.info(f"Response from token endpoint {response.text}")
    response_dict = json.loads(response.text)

    if 'access_token' in response_dict:
        app_access_token = response_dict['access_token']
        session['app_access_token'] = app_access_token
        return f"<p>Generated App Access Token: {readact_secret(app_access_token)}</p><br /><a href='/app_info'>Get App Info</a>"
    else:
        return "Failed to generate app access token!"

@app.route("/app_info")
def app_info():
    params = {
        "access_token": session.get('app_access_token')  # assuming the app access token is stored in the session
    }
    response = requests.get(f"https://graph.facebook.com/{FACEBOOK_APP_ID}", params=params)
    response_dict = json.loads(response.text)

    if 'error' not in response_dict:
        return jsonify(response_dict)
    else:
        return "Failed to get app info!"

def readact_secret(secret):
    return f"{secret[:10]}...{secret[-10:]}"


if __name__ == "__main__":
    app.run(debug=True, port=6789, host="localhost")