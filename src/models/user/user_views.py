from flask import Blueprint, redirect, render_template, request, session
from src.models.user.user import User

user_bp = Blueprint('user_blueprint', __name__)

@user_bp.route('/auth', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.is_login_valid(email, password):
            session['email'] = email
            return redirect('/')
        else:
            return "You entered the wrong email/password"
    return render_template('/')

@user_bp.route('/')
def login_form():
    session['email'] = None
    return render_template('user/login.html')

@user_bp.route('/logout')
def logout():
    session['email'] = None
    return render_template('login.html')

def logoutAll():
    session['email'] = None