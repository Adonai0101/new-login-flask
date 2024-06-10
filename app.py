from flask import Flask, request, jsonify, render_template,session,redirect,url_for,flash
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth
import json
from werkzeug.utils import secure_filename
from io import BytesIO

#Importamos mi propio modulo de login
from tools.login_required import login_required

#Blueprints
from routes.cuenta import cuenta


#Base de datos
from db import mongo

#Variables de entorno
from dotenv import load_dotenv
import os

# Cargar las variables de entorno del archivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Deberías usar una clave secreta segura
app.config["UPLOAD_FOLDER"] = "uploads"

# Configuración básica de Talisman, maneja las peticiones en https
#Talisman(app,force_https=True)

#Mongo db
app.config['MONGO_URI'] = os.getenv('URL_DB')
mongo.init_app(app)

# Configuración de Firebase
config = {
    "apiKey": "AIzaSyDI8o3e4SQ7443IgAenULNo289yWkaEn5M",
    "authDomain": "flask-firebase-auth-ad9fd.firebaseapp.com",
    "databaseURL": "https://YOUR_PROJECT_ID.firebaseio.com",
    "storageBucket": "flask-firebase-auth-ad9fd.appspot.com",
    "messagingSenderId": "1050060206485",
    "appId": "1:1050060206485:web:575fca153faa5a9d19c69c"
}

# diccionario de credenciales firebase

firebase_cred = {
    "type": os.getenv('FIREBASE_TYPE'),
    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
    "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
    "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL'),
    "universe_domain": os.getenv('FIREBASE_UNIVERSE_DOMAIN')
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
#cred = credentials.Certificate('flask-firebase-auth-.json')
cred = credentials.Certificate(firebase_cred)
firebase_admin.initialize_app(cred)


#Registro de blueprints
app.register_blueprint(cuenta, url_prefix='/cuenta')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():

    id_token = request.json.get('idToken')
    try:
        # Verificar el token con Firebase Admin SDK
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        user_info = decoded_token

        user = {
            'uid':uid,
            'nombre':user_info['name'],
            'email':user_info['email'],
            'foto':user_info['picture'],
            'telefono':""
        }

        result = mongo.db.user.find_one({'uid':uid})
        if not result:
            mongo.db.user.insert_one(user)

        result = mongo.db.user.find_one({'uid':uid})    
        result['_id'] = str(result['_id'])

        session['user'] = result

        respuesta = jsonify({"success": True, "uid": uid})
        respuesta.status_code = 200

        return respuesta
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)}), 400
    

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

#Subida de archivos a firebase
@app.route("/upload", methods=["POST"])
def upload_image():
    user = session.get("user")

    if "file" not in request.files:
        return jsonify({"error": "No se encontró el archivo"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No se seleccionó ningún archivo"}), 400

    file_extension = file.filename.split('.')[-1]
    archivos_permitidos = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "webp", "heic", "raw", "svg", "ico"]
    
    if file_extension not in archivos_permitidos:
        flash('¡Tipo de archivo incompatible!', 'error')
        return jsonify({"error": "Archivo no compatible"}), 400

    if file:
        filename = secure_filename(file.filename)
        extension = filename.split(".")[-1]
        filename = user['uid']+ "." + extension
        try:
            file_stream = BytesIO(file.read())  # Leer el archivo en un flujo de bytes

            # Sube el archivo a Firebase Storage directamente desde el flujo de bytes
            storage.child("images/" + filename).put(file_stream, file.content_type)
            url = storage.child("images/" + filename).get_url(None)

            return jsonify({
                "message": "Imagen subida exitosamente",
                'url':url,
                'filename':filename
            }), 200
        except Exception as e:
            print('error en el archivo')
            print({"error": str(e)})
            return jsonify({"error": str(e)}), 500  # Devuelve un mensaje de error y código 500 en caso de un error



@app.errorhandler(404)
@login_required
def pagina_no_encontrada(error):
    return render_template('404.html',user = session.get('user'))

@app.route('/panel')
@login_required
def dash_page():
    user = session.get('user')
    return render_template('panel/panel.html',user = user)




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
