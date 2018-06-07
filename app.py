from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from flask_oauthlib.client import OAuth, OAuthException
from logging import Logger
import uuid, json, requests, os

app = Flask(__name__)

app.secret_key = 'development'

port = os.environ['PORT']

oauth = OAuth(app)
microsoft = oauth.remote_app(
	'microsoft',
	consumer_key=os.environ['consumer_key'],
	consumer_secret=os.environ['consumer_secret'],
	request_token_params={'scope': ['files.readwrite.all','offline_access']},
	base_url='https://graph.microsoft.com/v1.0/',
	request_token_url=None,
	access_token_method='POST',
	access_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
	authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
)

## Inicio
@app.route('/')
def index():
	return render_template("index.html")

## Vista Previa
@app.route('/preview')
def preview():
	variable = microsoft.get('drive/root')
	return render_template('preview.html', variable=str(variable.data))

## Vista de árbol
@app.route('/tree')
def tree():
	tree = microsoft.get('drive/root/children')
	return render_template("tree.html", tree=str(tree.data))

## Subida simultanea
@app.route('/upload')
def upload():
	return render_template("upload.html")

## Contacto
@app.route('/contact')
def contact():
	return render_template("contact.html")

@app.route('/login/authorized')
def authorized():
	response = microsoft.authorized_response()

	if response is None:
		return "Access Denied: Reason=%s\nError=%s" % (
			response.get('error'), 
			request.get('error_description')
		)

	if str(session['state']) != str(request.args['state']):
		raise Exception('State has been messed with, end authentication')

	session['microsoft_token'] = (response['access_token'], '')
	print(session)
	print("session microsoft_token")
	print(session['microsoft_token'])
	return redirect(url_for('preview'))

## Inicio de sesión
@app.route('/login', methods = ['POST', 'GET'])
def login():
	if 'microsoft_token' in session:
		return redirect(url_for('preview'))
	
	guid = uuid.uuid4()
	session['state'] = guid
	#return microsoft.authorize(callback=url_for('authorized', _external=True), state=guid)
	return microsoft.authorize(callback='https://cloudsmanage.herokuapp.com/login/authorized', state=guid)

### Desconexión
@app.route('/logout')
def logout():
	session.pop('microsoft_token', None)
	session.pop('state', None)
	return redirect(url_for('index'))


#@microsoft.tokengetter
#def get_microsoft_oauth_token():
#	return session.get('microsoft_token')

@microsoft.tokengetter
def get_microsoft_oauth_token():
	return session.get('microsoft_token')

app.run('0.0.0.0', int(port), debug=True)