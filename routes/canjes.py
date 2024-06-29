from flask import Blueprint,jsonify, request,render_template,session,redirect,flash
from bson import json_util
from bson.objectid import ObjectId
import json
import random
#Mis herramientas
from tools.login_required import login_required
from tools.validaciones import *
from tools.get_user import *

#Base de datos
from db import mongo

canjes = Blueprint('canjes',__name__)

@canjes.route('/')
@login_required
def index_canjes():
    user = session.get('user')
    return render_template('canjes/canjear.html',user = user)

@canjes.route('/code',methods = ['POST'])
@login_required
def get_code():
    print('codigo a canjear')
    user = session.get('user')
    uid = user['uid']
    codigo = request.form['codigo']

    filtro = {
        '$and': [
            {'qr.uid': uid},
            {'codigo': codigo}
        ]
    }
    
    ticket = mongo.db.tarjeta.find_one(filtro)

    if ticket :
        mongo.db.tarjeta.delete_one(filtro)
        return redirect('/canjes/done')
    else:
        flash('¡Codigo no existe!', 'error')
        print('-No existe el ticket, o algo')
        return redirect('/canjes')

@canjes.route('/<id>')
@login_required
def one_canjes(id):
    user = session.get('user')
    ticket = mongo.db.tarjeta.find_one({'_id':ObjectId(id)})
    codigo = ticket['codigo']
    return render_template('canjes/codigo.html',user = user, codigo = codigo)


@canjes.route('/done')
@login_required
def conje_done():
    user = session.get('user')
    return render_template('canjes/canje_done.html',user = user)
