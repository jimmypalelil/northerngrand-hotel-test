from flask import Blueprint, render_template
from bson.json_util import dumps
from datetime import datetime

from src.common.database import Database

trial_bp = Blueprint('trial_blueprint', __name__)


@trial_bp.route('/trial')
def trial():
    return render_template('months/trial/trial.html', year = datetime.today().year)


@trial_bp.route('/trial/triallist')
def trialList():
    return render_template('months/trial/trialList.html')


@trial_bp.route('/pyList/<type>/<year>', methods=['GET'])
def returnList(type, year):
    rooms = Database.find(type, {"year": year})
    return dumps(rooms)
