'''Login with Github
Reference: https://docs.github.com/en/apps/creating-github-apps/writing-code-for-a-github-app/building-a-login-with-github-button-with-a-github-app
'''
import os
import requests
import logging
from flask import Flask, render_template, request, jsonify

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
app = Flask(__name__)

client_id = os.environ.get('GITHUB_CLIENT_ID')
client_secret = os.environ.get('GITHUB_CLIENT_SECRET')

@app.route('/')
def index():
	return render_template('index.html', client_id=client_id)

@app.route('/github/callback')
def github_calback():
	code = request.args.get('code')
	if code:
		# Exchange the code for an access token
		token_url = 'https://github.com/login/oauth/access_token'
		data = {
			'client_id': client_id,
			'client_secret': client_secret,
			'code': code
		}
		headers = {'Accept': 'application/json'}
		token_response = requests.post(token_url, data=data, headers=headers)
		log.info(f"Response for token exchange: {token_response.text}")

		if token_response.ok:
			access_token = token_response.json()['access_token']
			# Fetch user information
			user_url = 'https://api.github.com/user'
			headers = {'Authorization': f'Bearer {access_token}'}
			user_response = requests.get(user_url, headers=headers)
			log.info(f"Response for user details: {user_response.text}")

			if user_response.ok:
				user_data = user_response.json()
				# Do something with the user data
				return jsonify(user_data)
			else:
				# Handle error case when fetching user information fails
				return f'Error: Failed to fetch user information. Status code: {user_response.status_code}'
		else:
			# Handle error case when token exchange fails
			return f'Error: Failed to exchange code for access token. Status code: {token_response.status_code}'
	else:
		# Handle error case when code is not provided
		return 'Error: Code not received.'


if __name__ == '__main__':
	if client_id is None or client_secret is None:
		print("Please set CLIENT_ID and CLIENT_SECRET environment variables.")
	else:
		app.run(debug=True, port=4567)