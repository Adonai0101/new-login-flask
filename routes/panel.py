from flask import Blueprint,jsonify, request,render_template,session,redirect,flash
import json
#Mis herramientas
from tools.login_required import login_required
from tools.validaciones import *
from tools.get_user import *

#Base de datos
from db import mongo

panel = Blueprint('panel',__name__)

@panel.route('/')
@login_required
def dash_page():
    user = session.get('user')
    uid =  user['uid']
    tarjetas = mongo.db.tarjeta.find({'uid':uid})
    tarjetas = list(tarjetas)
    return render_template('panel/panel.html',user = user ,tarjetas = tarjetas)
