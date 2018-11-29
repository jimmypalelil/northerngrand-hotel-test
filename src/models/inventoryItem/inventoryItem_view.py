from flask import Blueprint, render_template, json, request, redirect
from bson.json_util import dumps
from src.common.database import Database
from src.models.inventoryItem.inventoryItem import InventoryItem

import src.models.user.decorators as user_decorators

inventory_bp = Blueprint('inventory_blueprint', __name__)

@inventory_bp.route('/')
@user_decorators.requires_login
def index():
    return render_template('inventory/inventory_home.html')

@inventory_bp.route('/new_item', methods=['GET', 'POST'])
def new_item():
    item_name = request.form['item_name'].strip()
    laundry = float(request.form['laundry'])
    lock_up = float(request.form['lock_up'])
    second = float(request.form['second'])
    third = float(request.form['third'])
    fourth = float(request.form['fourth'])
    fifth = float(request.form['fifth'])
    sixth = float(request.form['sixth'])
    par_stock = float(request.form['par_stock'])
    cost_per_item = float(request.form['cost_per_item'])
    par_25 = float(request.form['par_25'])
    type = request.form['type']
    InventoryItem(item_name, laundry, lock_up, second, third, fourth,
                  fifth, sixth, par_stock, cost_per_item, par_25, type).insert()
    return redirect('/inventory#!/inventorylist/' + type)

@inventory_bp.route('/delete/<id>', methods=['POST'])
def delete(id):
    InventoryItem.remove(id)
    return dumps(Database.DATABASE['inventory'].find())

@inventory_bp.route('/edit', methods=['GET','POST'])
def edit():
    data = json.loads(request.data)
    InventoryItem.update(data['_id'], data)
    return ''

@inventory_bp.route('/inventoryList/')
def inventoryList():
    return dumps(Database.DATABASE['inventory'].find())

@inventory_bp.route('/inventorylist')
def inventorylist():
    return render_template('inventory/inventoryList.html')