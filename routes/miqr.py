from flask import Blueprint,jsonify, request,render_template,session,redirect,flash
import json

#Base de datos
from db import mongo

#Mis herramientas
from tools.login_required import login_required
from tools.validaciones import *
from tools.get_user import *

miqr = Blueprint('miqr',__name__)

@miqr.route('/')
@login_required
def index():
    user = session.get('user')
    qr = mongo.db.qr.find_one({'uid':user['uid']})

    return render_template('usuario/qr.html',user = user, qr = qr)


@miqr.route('/add',methods = ['POST'])
@login_required
def create():
    user = session.get('user')
    datos = {
        'uid': user['uid'],
        'canjes': int(request.form['canjes']),
        'recompensa': request.form['recompensa'],
        'user':user
    }

    #Falta hacer validaciones
    if solo_numeros(request.form['canjes']) and is_nombre(request.form['recompensa']):

        resultado = mongo.db.qr.find_one({'uid':user['uid']})
        #Coprobamos si existe 
        if resultado:
            mongo.db.qr.update_one({'uid':user['uid']},{"$set":datos})
            #Modificando los datos para la tarjeta
            mongo.db.tarjeta.update_one({'qr.uid':user['uid']},{"$set":{
                'qr.uid': user['uid'],
                'qr.canjes': int(request.form['canjes']),
                'qr.recompensa': request.form['recompensa'],
                'qr.user':user
            }})

            flash('Tarjeta actualizada','success')
        else:
            mongo.db.qr.insert_one(datos)
            flash('Tarjeta registrada','success')
    else:
        flash('Error al ingresar los datos','error')

    return redirect('/miqr')