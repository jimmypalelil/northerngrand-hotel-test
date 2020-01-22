from flask import Blueprint, request, render_template, jsonify
from bson.json_util import dumps

from src.common.database import Database
from src.main import socketio

view_bp = Blueprint('view_blueprint', __name__)


@view_bp.route('/')
def home():
    return render_template('index.html')


@view_bp.route('/list/<type>/<year>/<month>')
def return_list(type, year, month):
    print(type, year, month)
    rooms = Database.find(type, {'year': year, 'month': month})
    return dumps(rooms)


@socketio.on('getLostList')
def return_lost_items(type):
    if type == 'lostItems':
        return dumps(Database.findAll('losts'))
    return dumps(Database.findAll('returned'))


@view_bp.route('/list/lost/<item_type>')
def return_lost_items(item_type):
    if item_type == 'lostItems':
        return dumps(Database.findAll('losts'))
    return dumps(Database.findAll('returned'))


@view_bp.route('/list/roomStatusChange', methods=['POST'])
def change_status():
    data = request.json
    rooms = data[0]
    status = data[1]
    for room in rooms:
        Database.DATABASE[room['cat']].update({'_id': room['_id']}, {"$set": {'status': status}})
    return jsonify({'text': 'STATUS CHANGED SUCCESSFULLY'})
