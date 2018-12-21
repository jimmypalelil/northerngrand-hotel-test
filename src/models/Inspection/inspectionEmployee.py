import uuid

from bson.json_util import dumps
from src.common.database import Database

collection = 'ins_employees'

class InspectionEmployee(object):
    def __init__(self, insId, empId,_id=None):
        self.insId = insId
        self.empId = empId
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "insId": self.insId,
            "empId": self.empId,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.update(collection, {"_id": self._id}, self.json())

    @classmethod
    def get_by_item_id(cls, id):
        return cls(**Database.find_one(collection, {"_id": id}))

    @classmethod
    def get_by_ins_id(cls, id):
        return Database.find(collection, {"insId": id})

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
    def getAllEmployees(insId):
        return dumps(Database.find(collection, {"insId": insId}))
