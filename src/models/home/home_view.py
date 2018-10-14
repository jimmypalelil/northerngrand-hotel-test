from flask import Blueprint, render_template
from datetime import datetime
import src.models.user.decorators as user_decorators

home_bp = Blueprint('home_blueprint', __name__)

@home_bp.route('/')
def home():
    return render_template('home.html', year = datetime.today().year)

@home_bp.route('/HK')
@user_decorators.requires_login
def HK():
    return render_template('HK/HK_Main.html')