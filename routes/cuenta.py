from flask import Blueprint,jsonify, request,render_template,session,redirect,flash
import json
#Mis herramientas
from tools.login_required import login_required
from tools.validaciones import *
from tools.get_user import *

#Base de datos
from db import mongo

cuenta = Blueprint('cuenta',__name__)

@cuenta.route('/', methods = ['GET'])
@login_required
def index(): 
    return render_template('usuario/perfil.html',user = session.get('user'))

@cuenta.route('/update',methods = ['POST'])
def cuenta_post():
    user_session = session.get("user")
    uid = user_session['uid']
    user = {
        'nombre': request.json['nombre'],
        'telefono': request.json['telefono']
    }
    print(user)
    #Validando los datos
    if is_nombre(user['nombre']) and is_telefono(user['telefono']):
    
        resultado = mongo.db.user.update_one({'uid':uid},{"$set":user}) 
        #modificando la informacion del qr segun el usuario
        resultado = mongo.db.qr.update_one({'uid':uid},{"$set":{
            'user.nombre':user['nombre'],
            'user.telefono':user['telefono'],
            }})
        
        get_user()
        flash('¡Usuario modificado con éxito!', 'success')
    else:
        flash('¡Error al ingresar los datos!', 'error')

    return jsonify({'msj':'usuario modificada con exito'}),200

@cuenta.route('/updatefoto',methods = ['POST'])
def update_foto():
    print('actualizando foto')
    user_session = session.get("user")
    uid = user_session['uid']
    data = request.json
    resultado = mongo.db.user.update_one({'uid':uid},{"$set":{'foto':data['url']}})
    get_user()
    flash('¡Foto actualizada!', 'success')
    print('se modifico bien la foto')
    return jsonify({'msj':'Foto modificada con exito'}),200