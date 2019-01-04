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
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(collection, {'_id': item_id}))

    @classmethod
    def get_by_item_cat(cls, item, cat):
        return Database.find_one(collection, {"item": item, 'cat': cat})

    @classmethod
    def update_item_name(cls, old, new):
        Database.DATABASE[collection].update({'item': old}, {'$set': {'item': new}})

    @classmethod
    def update_cat_name(cls, old, new):
        Database.DATABASE[collection].update({'cat': old}, {'$set': {'cat': new}})

    @classmethod
    def insert(cls, item, cat):
        temp = InspectionItem.get_by_item_cat(item, cat)
        if temp is None:
            InspectionItem(item, cat).save_to_mongo()

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