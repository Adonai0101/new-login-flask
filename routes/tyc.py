from flask import Blueprint,render_template,session,json,jsonify,request

tyc = Blueprint('tyc',__name__)

@tyc.route('/')
def tyc_page():
    return render_template('tyc/tyc.html')
