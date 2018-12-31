import uuid

from bson.json_util import dumps
from src.common.database import Database

collection = 'ins_scores'

class InspectionScore(object):
    def __init__(self, insId, itemId, score, comment,_id=None):
        self.insId= insId
        self.itemId = itemId
        self.score = score
        self.comment = comment
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "insId": self.insId,
            "itemId": self.itemId,
            "score": self.score,
            "comment": self.comment,
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
    def remove_by_insId(cls, insId):
        Database.remove(collection, {"insId": insId})

    @classmethod
    def updateEmployee(cls, id, data):
        Database.update(collection, {"_id": id}, data)

    @staticmethod
    def getAllEmployees():
        return dumps(Database.findAll(collection))