import uuid

from bson.json_util import dumps
from src.common.database import Database

collection = 'inspections'

class Inspection(object):
    def __init__(self, room_number, day, month, year, score, _id=None):
        self.room_number = room_number
        self.day = day
        self.month = month
        self.year = year
        self.score = score
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "room_number": self.room_number,
            "month": self.month,
            "day": self.day,
            "year": self.year,
            "score": self.score,
            "_id": self._id
        }

    def updateSelf(self):
        Database.update(collection, {"_id": self._id}, self.json())

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(collection, {"_id": id}))

    def insert(self):
        Database.insert(collection, self.json())

    @classmethod
    def remove(cls, id):
        Database.remove(collection, {"_id": id})


    @classmethod
    def update(cls, id, data):
        Database.update(collection, {"_id": id}, data)

    def insertOne(self):
        return Database.insertOne(collection, self.json())

    @staticmethod
    def getAllEmployees():
        return dumps(Database.findAll(collection))

    @classmethod
    def getInspectionItems(cls, insID, day, month, year):
        pipeline = [{
            "$match": {
                "_id": insID,
                "day": day,
                "month": month,
                "year": year
            }
        }, {
            "$lookup": {
                'from': "ins_scores",
                'localField': "_id",
                'foreignField': "insId",
                'as': "item"
            }
        }, {
            "$unwind": "$item"
        },{
            "$lookup": {
                'from': "ins_items",
                'localField': "item.itemId",
                'foreignField': "_id",
                'as': "inspection"
            }
        }, {
            "$unwind": "$inspection"
        }, {
            "$group": {
                "_id": "$inspection.cat",
                "items": { "$push": "$$ROOT"}
            }
        }]
        return dumps(Database.DATABASE[collection].aggregate(pipeline))