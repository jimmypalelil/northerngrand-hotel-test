import uuid

from bson.json_util import dumps
from src.common.database import Database

collection = 'employees'

class Employee(object):
    def __init__(self, name, avg_score, num_inspections,_id=None):
        self.name = name
        self.avg_score = avg_score
        self.num_inspections = num_inspections
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "name": self.name,
            "avg_score": self.avg_score,
            "num_inspections": self.num_inspections,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.update(collection, {"_id": self._id}, self.json())

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(collection, {"_id": id}))

    def insert(self):
        Database.insert(collection, self.json())

    @classmethod
    def remove(cls, id):
        Database.remove(collection, {"_id": id})


    def update(self):
        Database.update(collection, {"_id": self._id}, self.json())

    @classmethod
    def updateEmployee(cls, id, data):
        Database.update(collection, {"_id": id}, data)

    @staticmethod
    def getAllEmployees():
        return dumps(Database.findAll(collection))

    @classmethod
    def getMonthlyInspections(cls, empID):
        pipeline = [{
             "$lookup": {
                'from': "ins_monthly_scores",
                'localField': "_id",
                'foreignField': "empId",
                'as': "Monthly Scores"}
        }, {
            "$match": {
                "_id": empID
            }
        }]
        return dumps(Database.DATABASE[collection].aggregate(pipeline))

    @classmethod
    def getEmployeeInspections(cls, empID):
        pipeline = [{
            "$match": {
                "_id": empID
                }
            }, {
            "$lookup": {
                'from': "ins_employees",
                'localField': "_id",
                'foreignField': "empId",
                'as': "empInspections"
                }
            },  {
           "$lookup": {
               'from': "inspections",
               'localField': "empInspections.insId",
               'foreignField': "_id",
               'as': "inspections"
           }
        }]
        return dumps(Database.DATABASE[collection].aggregate(pipeline))
