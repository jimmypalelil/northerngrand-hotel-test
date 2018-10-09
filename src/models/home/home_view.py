from flask import Blueprint, render_template, session
from datetime import datetime
import src.models.user.decorators as user_decorators


home_bp = Blueprint('home_blueprint', __name__)

@home_bp.route('/')
def home():
    print(session)
    return render_template('home.html', year = datetime.today().year)

@home_bp.route('/bedding')
@user_decorators.requires_login
def bedding_page():
    if session['email'] == 'jimmypalelil@gmail.com' or session['email'] == 'housekeeping@northerngrand.ca':
        return render_template('months/bedding/bedding.html', year = datetime.today().year)
    return render_template('user/login.html', message = "Access to Housekeeping only")

@home_bp.route('/carpet_shampoo')
@user_decorators.requires_login
def carpet_shampoo_page():
    if session['email'] == 'jimmypalelil@gmail.com' or session['email'] == 'housekeeping@northerngrand.ca':
        return render_template('months/carpet_shampoo/carpet_shampoo.html', year = datetime.today().year)
    return render_template('user/login.html', message = "Access to Housekeeping only")

@home_bp.route('/pillow_protector')
@user_decorators.requires_login
def pillow_protector_page():
    if session['email'] == 'jimmypalelil@gmail.com' or session['email'] == 'housekeeping@northerngrand.ca':
        return render_template('months/pillow_protector/pillow_protector.html', year = datetime.today().year)
    return render_template('user/login.html', message = "Access to Housekeeping only")

@home_bp.route('/mattresss')
@user_decorators.requires_login
def mattress_page():
    if session['email'] == 'jimmypalelil@gmail.com' or session['email'] == 'housekeeping@northerngrand.ca':
        return render_template('months/mattress/mattress.html', year=datetime.today().year)
    return render_template('user/login.html', message = "Access to Housekeeping only")

@home_bp.route('/pillowss')
@user_decorators.requires_login
def pillows_page():
    if session['email'] == 'jimmypalelil@gmail.com' or session['email'] == 'housekeeping@northerngrand.ca':
        return render_template('months/pillows/pillows.html', year=datetime.today().year)
    return render_template('user/login.html', message = "Access to Housekeeping only")
