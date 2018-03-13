from flask import Blueprint, json, request, redirect
from bson.json_util import dumps

from src.common.database import Database

trial_status_bp = Blueprint('trial_staus_blueprint', __name__)


@trial_status_bp.route('/<type>', methods  =['POST', 'GET'])
def doneroom(type):
    data = json.loads(request.data)
    for id in data:
        room = Database.find_one(type, {"_id": id})
        room['status'] = 'clean' if room['status'] == 'not done' else 'not done'
        Database.update(type, {"_id": id}, room)
    return ''
