import uuid, datetime

from bson.json_util import dumps
from src.common.database import Database
from src.models.item.item import Item

collection = 'returned'

class ReturnedItem(object):
    def __init__(self, room_number, guest_name, item_description, returned_by, date_found, comments, return_date, _id=None):
        self.room_number = room_number
        self.guest_name = guest_name
        self.item_description = item_description
        self.returned_by = returned_by
        self.return_date = return_date
        self.date_found = date_found
        self.comments = comments
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "room_number": self.room_number,
            "guest_name": self.guest_name,
            "item_description": self.item_description,
            "returned_by": self.returned_by,
            "return_date": self.return_date,
            "date_found": self.date_found,
            "comments":self.comments,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.update(collection, {"_id": self._id}, self.json())

    @classmethod
    def get_by_item_id(cls, id):
        return cls(**Database.find_one(collection, {"_id": id}))

    def insert(self):
        Database.insert(collection, self.json())

    @classmethod
    def remove(cls, id):
        Database.remove(collection, {"_id": id})

    @classmethod
    def update(cls, id, data):
        Database.update(collection, {"_id": id}, data)

    @classmethod
    def updateReturn(cls, id, data):
        Database.update(collection, {"_id": id}, data)

    @classmethod
    def deleteReturn(cls, id):
        item = ReturnedItem.get_by_item_id(id)
        Item(item.room_number, item.item_description, item.date_found, _id=item._id).insert()
        Database.remove(collection, {"_id": id})

    @classmethod
    def createNewReturn(cls, id, guestName, returnedBy, return_date, comments):
        item = Item.get_by_item_id(id)
        Item.remove(id)
        ReturnedItem(item.room_number, guestName, item.item_description, returnedBy, item.date, comments, return_date, item._id).insert()

    @staticmethod
    def getAllReturned():
        return dumps(Database.findAll('returned'))