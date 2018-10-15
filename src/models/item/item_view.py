from flask import Blueprint, render_template, json, request, redirect, session, url_for
from bson.json_util import dumps
from src.common.database import Database
from src.models.item.item import Item
from src.models.item.returnedItem import ReturnedItem
from datetime import datetime

import sendgrid, os
from sendgrid.helpers.mail import *

import src.models.user.decorators as user_decorators

item_bp = Blueprint('lost_and_found', __name__)


@item_bp.route('/', methods=['GET','POST'])
@user_decorators.requires_login
def index():
    if request.method == 'POST':
        room_number = request.form['room_number'].strip()
        item_description = request.form['item_description'].strip()
        date = request.form['date']
        Item(room_number, item_description, date).insert()
        return redirect('/lostAndFound/')

    return render_template('lostAndFound/lostAndFound_home.html', date= datetime.today().strftime("%Y-%m-%d"))


@item_bp.route('/returnListView' , methods=['GET', 'POST'])
def returnListView():
    return render_template('lostAndFound/ViewReturned.html', date = datetime.today().strftime("%Y-%m-%d"))


@item_bp.route('/returnList')
def returnList():
    return dumps(Database.findAll('returned'))

@item_bp.route('/returnItem', methods=['POST'])
def returnItem():
    id = request.form['itemID']
    guestName = request.form['guestName']
    returnedBy = request.form['returnedBy']
    comments = request.form['comments']
    ReturnedItem.createNewReturn(id, guestName, returnedBy, comments)
    return redirect('/lostAndFound/')


@item_bp.route('/deleteLostItem/<id>', methods=['GET', 'POST'])
def deleteLostItem(id):
    Item.remove(id)
    return Item.getAllLosts()

@item_bp.route('/deleteReturnedItem/<id>', methods=['GET', 'POST'])
def deleteReturnedItem(id):
    ReturnedItem.remove(id)
    return ReturnedItem.getAllReturned()


@item_bp.route('/edit/<id>', methods=['GET','POST'])
def edit(id):
    data = json.loads(request.data)
    Item.update(id, data)
    return redirect('/lostAndFound/')


@item_bp.route('/editReturn/<id>', methods=['GET','POST'])
def editReturn(id):
    data = json.loads(request.data)
    ReturnedItem.updateReturn(id, data)
    return redirect('/lostAndFound/returnListView')


@item_bp.route('/lostList')
def lostList():
    return dumps(Database.find('losts', {"cat": "losts"}))


@item_bp.route('/undoReturn/<id>', methods=['POST'])
def undoReturn(id):
    ReturnedItem.deleteReturn(id)
    return (ReturnedItem.getAllReturned())


@item_bp.route('/emailItem/<id>', methods=['POST'])
def email(id):
    item = Item.get_by_item_id(id)
    sendMail(item)
    return ''


def sendMail(item):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("reservations@northerngrand.ca")
    subject = 'Item Request from Front Desk'
    to_email = Email("housekeeping@northerngrand.ca", "jimmypalelil@gmail.com")
    msg = 'Front Desk has requested the following Item:     ' + \
        'Item Description: ' + item.item_description + \
        '|  Room No.: ' + item.room_number + \
        '|  Date Found: ' + item.date
    content = Content("text/plain", msg)
    mail = Mail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=mail.get())