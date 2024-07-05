from flask import Blueprint,render_template,session,json,jsonify,request
#Mis herramientas
from tools.login_required import login_required
from tools.validaciones import *
from tools.get_user import *
from tools.codigo import *

from bson import json_util
from bson.objectid import ObjectId

#Base de datos
from db import mongo

scaner = Blueprint('scaner',__name__)

@scaner.route('/')
@login_required
def index():
    return render_template('scaner/scaner.html',user = session.get('user'))


#pantallas para mostar si tuvimos un error o fue exitoso
@scaner.route('/done')
@login_required
def scaner_done():
    return render_template('scaner/done.html',user = session.get('user'))



@scaner.route('/error')
@login_required
def scaner_error():
    return render_template('scaner/error.html',user = session.get('user'))

@scaner.route('/api',methods = ['POST'])
def read_code():
    user = session.get("user")
    uid = user['uid']
    #Este 'codigo' es oara hacer el canje del ticket
    codigo = gen_code()

    code = request.json['codigo']
    print('Scaner QR')
    print(code)
    try:
        resultado = mongo.db.qr.find_one({'_id':ObjectId(code)})
  
        if resultado:
            filtro = {
                '$and': [
                    {'qr._id': ObjectId(code)},
                    {'uid': uid}
                ]
            }
            consulta = mongo.db.tarjeta.find_one(filtro)
            if consulta:
                actualizacion = {'$inc': {'canjes': 1}}
                mongo.db.tarjeta.update_one(filtro,actualizacion)
                print('SI tenemos tarjeta incrementar')
            else:
                print('NO tenemos tarjeta generar una nueva')
                tarjeta = {
                    'fecha':"", #Agregar la fecha no mms
                    'canjes':1,
                    'uid':user['uid'],
                    'qr':resultado,
                    'codigo':codigo
                }
                mongo.db.tarjeta.insert_one(tarjeta)
                print(tarjeta)
            return jsonify({'msj':'ehevh'}),200
        else:
            return jsonify({'msj':'caca'}),500
    except:
        print('codigo fallido')
        return jsonify({'msj':'caca'}),500