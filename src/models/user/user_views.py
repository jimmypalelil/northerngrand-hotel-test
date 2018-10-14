from flask import Blueprint, redirect, render_template, request, session
from src.models.user.user import User
import sendgrid, os, datetime, requests, pytz
from sendgrid.helpers.mail import *

user_bp = Blueprint('user_blueprint', __name__)

@user_bp.route('/auth', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.is_login_valid(email, password):
            session['email'] = email
            if email != 'jimmypalelil@gmail.com':
                sendMail(email)
            if email == 'reservations@northerngrand.ca':
                sendSMS(email)
                return redirect ('/lostAndFound')
            return redirect('/')
        else:
            return "You entered the wrong email/password"
    return render_template('user/login.html')

def sendMail(email):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("info@northerngrand.ca")
    subject = email + ": Signin INFO"
    to_email = Email("jimmypalelil@gmail.com")
    utc = pytz.timezone('Canada/Pacific')
    date_time = utc.localize(datetime.datetime.now())
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    content = Content("text/plain", email + " signed in on: " + date_time.strftime('%Y-%m-%d') + " at: " + date_time.strftime('%H:%M') + \
              "\nIP Address: " + ip)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

def sendSMS(email):
    TILL_URL = os.environ.get('TILL_URL')
    utc = pytz.timezone('Canada/Pacific')
    date_time = utc.localize(datetime.datetime.now())
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    msg = email + " signed in on: " + date_time.strftime('%Y-%m-%d') + " at: " + date_time.strftime('%H:%M') + \
        "\nIP Address: " + ip
    requests.post(TILL_URL, json={
        "phone": ["+16047041312"],
        "text": msg
    })
    
@user_bp.route('/')
def login_form():
    session['email'] = None
    return render_template('user/login.html')

@user_bp.route('/logout')
def logout():
    session['email'] = None
    return render_template('user/login.html')

def logoutAll():
    session['email'] = None
