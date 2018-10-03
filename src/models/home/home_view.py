from flask import Blueprint, render_template, session
from datetime import datetime

home_bp = Blueprint('home_blueprint', __name__)

@home_bp.route('/')
def home():    
    return render_template('home.html', year = datetime.today().year)

@home_bp.route('/bedding')
def bedding_page():
    if session['email'] == 'jimmypalelil@gmail.com' or session['email'] == 'housekeeping@northerngrand.ca':
        return render_template('months/bedding/bedding.html', year = datetime.today().year)
    return render_template('user/login.html', message = "Access to Housekeeping only")

@home_bp.route('/carpet_shampoo')
def carpet_shampoo_page():
    if session['email'] == 'jimmypalelil@gmail.com' or session['email'] == 'housekeeping@northerngrand.ca':
        return render_template('months/carpet_shampoo/carpet_shampoo.html', year = datetime.today().year)
    return render_template('user/login.html', message = "Access to Housekeeping only")

@home_bp.route('/pillow_protector')
def pillow_protector_page():
    if session['email'] == 'jimmypalelil@gmail.com' or session['email'] == 'housekeeping@northerngrand.ca':
        return render_template('months/pillow_protector/pillow_protector.html', year = datetime.today().year)
    return render_template('user/login.html', message = "Access to Housekeeping only")

@home_bp.route('/mattresss')
def mattress_page():
    if session['email'] == 'jimmypalelil@gmail.com' or session['email'] == 'housekeeping@northerngrand.ca':
        return render_template('months/mattress/mattress.html', year=datetime.today().year)
    return render_template('user/login.html', message = "Access to Housekeeping only")

@home_bp.route('/pillowss')
def pillows_page():
    if session['email'] == 'jimmypalelil@gmail.com' or session['email'] == 'housekeeping@northerngrand.ca':
        return render_template('months/pillows/pillows.html', year=datetime.today().year)
    return render_template('user/login.html', message = "Access to Housekeeping only")
