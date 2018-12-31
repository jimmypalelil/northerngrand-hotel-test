from flask import Blueprint, json, request
from src.common.database import Database

trial_status_bp = Blueprint('trial_staus_blueprint', __name__)


@trial_status_bp.route('/<type>/<status>', methods  =['POST', 'GET'])
def doneroom(type, status):  # Gets a list of rooms
    data = json.loads(request.data)
    for id in data:
        room = Database.find_one(type, {"_id": id})
        room['status'] = status
        Database.update(type, {"_id": id}, room)
    return ''
