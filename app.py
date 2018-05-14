from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from flask_oauthlib.client import OAuth, OAuthException
from logging import Logger
import uuid
import json

app = Flask(__name__)

app.secret_key = 'development'
oauth = OAuth(app)
microsoft = oauth.remote_app(
	'microsoft',
	consumer_key='d9694d49-12a5-4f88-a654-26c13ae05599',
	consumer_secret='tyxdmOQHNI48@@paIX639}{',
	request_token_params={'scope': 'offline_access User.Read'},
	base_url='https://graph.microsoft.com/v1.0/',
	request_token_url=None,
	access_token_method='POST',
	access_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
	authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
)



## Inicio

@app.route('/')
def inicio():
	return render_template("index.html")



## Inicio de sesión

@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'microsoft_token' in session:
		## Cambiar el 'me'
		return redirect(url_for('me'))
	
	guid = uuid.uuid4()
	session['state'] = guid

	return microsoft.authorize(callback=url_for('authorized', _external=True), state=guid)



## Desconexión

@app.route('/logout')
def logout():
	session.pop('microsoft_token', None)
	session.pop('state', None)
	## Cambiar el 'index'
	return redirect(url_for('index'))


@microsoft.tokengetter
def get_microsoft_oauth_token():
	return session.get('microsoft_token')

if __name__ == '__main__':
	app.debug = True
	app.run()