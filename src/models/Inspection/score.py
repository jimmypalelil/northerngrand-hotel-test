import uuid

from bson.json_util import dumps
from src.common.database import Database

collection = 'ins_monthly_scores'

class Score(object):
    def __init__(self, empId, month, year, score, num_inspections=None, _id=None):
        self.empId = empId
        self.month = month
        self.year = year
        self.score = score
        self.num_inspections = 1 if num_inspections is None else num_inspections
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "empId": self.empId,
            "month": self.month,
            "year": self.year,
            "num_inspections": self.num_inspections,
            "score": self.score,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.update(collection, {"_id": self._id}, self.json())

    @classmethod
    def get_by_item_id(cls, id):
        return cls(**Database.find_one(collection, {"_id": id}))

    @classmethod
    def get_by_emp_id(cls, id, month):
        return Database.find_one(collection, {"empId": id, "month": month})

    def insert(self):
        Database.insert(collection, self.json())

    @classmethod
    def remove(cls, id):
        Database.remove(collection, {"_id": id})

    @classmethod
    def remove_by_empId_and_month(cls, empId, month):
        Database.remove(collection, {"empId": empId, "month": month})


    @classmethod
    def updateScore(cls, empId, month, data):
        Database.update(collection, {"empId": empId, "month": month}, data)

    @staticmethod
    def getAllEmployees():
        return dumps(Database.findAll(collection))