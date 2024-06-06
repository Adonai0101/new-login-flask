from flask import session
from db import mongo

def get_user():

    user_session = session.get("user")
    uid = user_session['uid']
    #generando la informacion del usuario para mostrar en interfaz
    resultado = mongo.db.user.find_one({'uid':uid})
    resultado['_id'] = str(resultado['_id'])
    session["user"] = resultado