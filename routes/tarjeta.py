from flask import Blueprint,jsonify, request,render_template,session,redirect,flash
import json

#Base de datos
from db import mongo

#Mis herramientas
from tools.login_required import login_required
from tools.validaciones import *
from tools.get_user import *

tarjeta = Blueprint('tarjeta',__name__)

@tarjeta.route('/')
@login_required
def index():
    print('tarjeta')
    user_session = session.get("user")
    uid = user_session['uid']
    resultado = mongo.db.qr.find_one({'uid':uid})
    print(resultado)

    if resultado:
        resultado['_id'] = str(resultado['_id'])

        return render_template('usuario/tarjeta.html',user = session.get('user'),qr = resultado)

    else:
        return render_template('usuario/tarjeta_error.html',user = session.get('user'),qr = resultado)

        