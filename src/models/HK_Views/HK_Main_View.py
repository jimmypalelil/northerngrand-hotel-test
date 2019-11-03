from flask import Blueprint, render_template
from bson.json_util import dumps

from src.common.database import Database

hk_bp = Blueprint('hk_blueprint', __name__)


@hk_bp.route('/HK_Views/hkList')
def trialList():
    return render_template('HK/HK_List.html')


@hk_bp.route('/pyList/<type>/<year>/<month>', methods=['GET'])
def returnList(type, year, month):
    rooms = Database.find(type, {"month": month, "year": year})
    return dumps(rooms)
