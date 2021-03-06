from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from flask_oauthlib.client import OAuth, OAuthException
from logging import Logger
import uuid, json, requests, os, funciones, onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer

app = Flask(__name__)

app.secret_key = 'development'
port = os.environ['PORT']
UPLOAD_FOLDER = './upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
	if "state" in session:
		login=True
	else:
		login=False
	return render_template("index.html",login=login)

## Vista Previa
@app.route('/preview')
def preview():
	dic = microsoft.get('me/drive').data

	user=dic["owner"]["user"]["displayName"]
	total=funciones.AjustarUnidad(dic["quota"]["total"])
	usado=funciones.AjustarUnidad(dic["quota"]["used"])
	libre=funciones.AjustarUnidad(dic["quota"]["remaining"])

	return render_template('preview.html', user=user,total=total,usado=usado,libre=libre)

## Vista de árbol
@app.route('/tree/<idcarpeta>')
def tree(idcarpeta):
	if idcarpeta == "root":
		tree = microsoft.get('drive/root/children').data
	else:
		tree=microsoft.get('me/drive/items/%s/children'%(idcarpeta)).data

#	tree=[]
#	subcarpetas=[]

#	tree,subcarpetas=funciones.FormarArbol(dic,tree,subcarpetas)
#	for nivel in subcarpetas:
#		for elem in nivel:
#			dic=microsoft.get('me/drive/items/%s/children'%(elem)).data
#			tree,subcarpetas=funciones.FormarArbol(dic,tree,subcarpetas)

	return render_template('tree.html', tree=tree)
	
## Subida de Fichero
@app.route('/upload', methods = ['POST', 'GET'])
def upload():
	return render_template("upload.html",uploaded=False)
	if request.method == "POST":
		redirect_uri = 'https://cloudsmanage.herokuapp.com/upload'
		client_secret = os.environ['consumer_secret']
		scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']
		client = onedrivesdk.get_default_client(client_id=os.environ['consumer_key'], scopes=scopes)
		auth_url = client.auth_provider.get_auth_url(redirect_uri)
		code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
		client.auth_provider.authenticate(code, redirect_uri, client_secret)
		file = request.files['file']
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		returned_item = client.item(drive='me', id='root').children[filename].upload('./upload/%s'%(file.filename))
		
		return render_template("upload.html",uploaded=True)
	else:
		return render_template("upload.html",uploaded=False)

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
	return redirect(url_for('index'))

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