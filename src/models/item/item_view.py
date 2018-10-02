from flask import Blueprint, render_template, json, request, redirect, session
from bson.json_util import dumps
from src.common.database import Database
from src.models.item.item import Item
from datetime import datetime

item_bp = Blueprint('lost_and_found', __name__)

@item_bp.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        room_number = request.form['room_number'].strip()
        item_description = request.form['item_description'].strip()
        date = request.form['date']
        Item(room_number, item_description, date).insert()
        return redirect('/lostAndFound/')

    if session['email'] != 'None':
        return render_template('/lostAndFound/lostAndFound_home.html', date= datetime.today().strftime("%Y-%m-%d"))
    return render_template('/user/login.html')


@item_bp.route('/edit/<id>', methods=['GET','POST'])
def edit(id):
    item = Item.get_by_room_id(id)
    data = json.loads(request.data)
    item.update(data['_id'], data)
    return redirect('/lostAndFound/')


@item_bp.route('/lostList')
def lostList():
    return dumps(Database.find('losts', {"cat": "losts"}))


@item_bp.route('/returned/<id>' , methods = ['POST'])
def returned(id):
    item = Item.get_by_room_id(id)
    item.remove(id)
    return dumps(Database.find('losts', {"cat": "losts"}))
