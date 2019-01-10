from flask import Blueprint, request, render_template, redirect, make_response, jsonify
from bson.json_util import dumps

from src.common.database import Database

view_bp = Blueprint('view_blueprint', __name__)


@view_bp.route('/')
def home():
    return render_template('index.html')

@view_bp.route('/list/<type>/<year>/<month>')
def returnList(type, year, month):
    rooms = Database.find(type, {'year': year, 'month': month})
    return dumps(rooms)

@view_bp.route('/list/lost/<type>')
def returnLostItems(type):
    if(type == 'lostItems'):
        return dumps(Database.findAll('losts'))
    return dumps(Database.findAll('returned'))

@view_bp.route('/list/roomStatusChange', methods=['POST'])
def changeStatus():
    data = request.json
    rooms = data[0]
    status = data[1]
    for room in rooms:
        Database.DATABASE[room['cat']].update({'_id': room['_id']}, {"$set": {'status': status}})
        # Database.update(room['cat'], {'_id': room['_id']}, room)
    return jsonify({'text': 'STATUS CHANGED SUCCESSFULLY'})
