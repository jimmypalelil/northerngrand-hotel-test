from flask import Blueprint, request, render_template, redirect, make_response, jsonify
from bson.json_util import dumps
from src.models.room import room

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
    room = request.json
    if(room['status'] == 'clean'):
      room['status'] = 'not done'
    else:
      room['status'] = 'clean'
    Database.update(room['cat'], {'_id': room['_id']}, room)
    return jsonify({'text': 'STATUS CHANGED SUCCESSFULLY'})
