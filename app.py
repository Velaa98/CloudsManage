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
	variable = microsoft.get('me/drive')
	return render_template('preview.html', variable=str(variable.data))

## Vista de árbol
@app.route('/tree')
def tree():
	dic = microsoft.get('drive/root/children').data
	tree = []
	for elem in dic["value"]:
		# Si el path es root entra en el elemento 0 de tree.
		if elem["parentReference"]["path"] == "/drive/root:":
			# Si La lista tree aún no tiene elementos crea el primero. 
			if len(tree) == 0:
				tree.append({})
			
			# Si hay una carpeta en el nivel,
			if "folder" in elem:
				# Y aún no existe el diccionario folders, lo crea y añade a la lista uno nuevo con el nombre de la carpeta.
				if "folders" not in tree[0]:
					tree[0]["folders"]=[]
					tree[0]["folders"].append(dict(name=elem["name"]))
				# si existe añade a la lista de folders un nuevo diccionario con el nombre de la carpeta.
				else:
					tree[0]["folders"].append(dict(name=elem["name"]))
				# si la carpeta tiene carpetas dentro:
				if elem["folder"]["childCount"] > 0:
					# Se recorren las carpetas que hay en el nivel 0
					for i in tree[0]["folders"]:
						# Cuando la carpeta sea la que estamos tratando,
						if i["name"] == elem["name"]:
							# Añade un nuevo valor al diccionario con formato: "NumCarpetas"= X
							i["childCount"]=elem["folder"]["childCount"]

			# Si hay un fichero en el nivel,
			if "file" in elem:
				# Y aún no existe el diccionario files, lo crea y añade a la lista uno nuevo con el nombre del fichero.
				if "files" not in tree[0]:
					tree[0]["files"]=[]
					tree[0]["files"].append(dict(name=elem["name"]))	
				# si existe añade a la lista de files un nuevo diccionario con el nombre del fichero.
				else:
					tree[0]["files"].append(dict(name=elem["name"]))
	return render_template("tree.html", tree=str(tree))

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