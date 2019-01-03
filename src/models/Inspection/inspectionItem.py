import uuid

from bson.json_util import dumps
from src.common.database import Database

collection = 'ins_items'

class InspectionItem(object):
    def __init__(self, item, cat, _id=None):
        self.item = item
        self.cat = cat
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "item": self.item,
            "cat": self.cat,
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
    def updateEmployee(cls, id, data):
        Database.update(collection, {"_id": id}, data)

    @staticmethod
    def getAllItems():
        return Database.findAll(collection)

    @staticmethod
    def getAllItemsByGroup():
        pipeline = [{
            "$group": {
                "_id": {"cat": "$cat"},
                "items": {"$push": "$$ROOT"}
            }
        }]
        return dumps(Database.DATABASE[collection].aggregate(pipeline))