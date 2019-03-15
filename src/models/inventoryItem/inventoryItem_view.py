from flask import Blueprint, render_template, json, request, jsonify
from bson.json_util import dumps
from src.models.inventoryItem.inventoryItem import InventoryItem

import src.models.user.decorators as user_decorators

inventory_bp = Blueprint('inventory_blueprint', __name__)

@inventory_bp.route('/')
@user_decorators.requires_login
def index():
    return render_template('inventory/inventory_home.html')


@inventory_bp.route('/newItem', methods=['POST'])
def new_item():
    item = request.json
    item_name = item['item_name'].strip()
    laundry = float(item['laundry'])
    lock_up = float(item['lock_up'])
    second = float(item['second'])
    third = float(item['third'])
    fourth = float(item['fourth'])
    fifth = float(item['fifth'])
    sixth = float(item['sixth'])
    par_stock = float(item['par_stock'])
    cost_per_item = float(item['cost_per_item'])
    par_25 = float(item['par_25'])
    type = item['type']
    InventoryItem(item_name, laundry, lock_up, second, third, fourth,
                  fifth, sixth, par_stock, cost_per_item, par_25, type).insert()
    return jsonify({'text': "Item Added Successfully!!!"})


@inventory_bp.route('/deleteItem/<id>', methods=['GET'])
def delete(id):
    InventoryItem.remove(id)
    return jsonify({'text': "Item Was Deleted Successfully!!!"})


@inventory_bp.route('/editItem', methods=['GET','POST'])
def edit():
    data = json.loads(request.data)
    InventoryItem.update(data['_id'], data)
    return jsonify({'text': "Item Was Updated Successfully!!!"})


@inventory_bp.route('/inventoryList/')
def inventory_list():
    return dumps(InventoryItem.get_inventory_items())