from flask import Blueprint,render_template,session,json,redirect

from bson import json_util
from bson.objectid import ObjectId

#Mis herramientas
from tools.login_required import login_required
from tools.validaciones import *
from tools.get_user import *

#DB 
from db import mongo

tickets = Blueprint('tickets',__name__)

@tickets.route('/')
@login_required
def index():
    user = session.get('user')
    uid =  user['uid']
    tarjetas = mongo.db.tarjeta.find({'uid':uid})
    tarjetas = list(tarjetas)

    return render_template('tickets/tickets.html',user = user ,tarjetas = tarjetas)

@tickets.route('/<id>')
@login_required
def one_ticket(id):
    user = session.get('user')
    tarjeta = mongo.db.tarjeta.find_one({'_id':ObjectId(id)})
    return render_template('tickets/ticket.html',user = user ,tarjeta = tarjeta)
