import uuid

from bson.json_util import dumps
from src.common.database import Database
from src.models.Inspection.employeemonthlyscore import EmployeeMonthlyScore

collection = 'employees'

class Employee(object):
    def __init__(self, name, avg_score, total_score, num_inspections, _id=None):
        self.name = name
        self.avg_score = avg_score
        self.total_score = total_score
        self.num_inspections = num_inspections
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "name": self.name,
            "avg_score": self.avg_score,
            "total_score": self.total_score,
            "num_inspections": self.num_inspections,
            "_id": self._id
        }

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
    def update_emp(cls, id, data):
        Database.update(collection, {"_id": id}, data)

    @classmethod
    def update_emp_score(cls, empId, total_score, count):
        Database.DATABASE[collection].update({"_id": empId}, {'$inc': {'total_score': total_score,
                                                                       'num_inspections': count}})

    @staticmethod
    def get_all_emps():
        return Database.findAll(collection)

    @classmethod
    def get_monthly_inspections(cls, emp_id):
        pipeline = [{
             "$lookup": {
                'from': "ins_monthly_scores",
                'localField': "_id",
                'foreignField': "emp_id",
                'as': "Monthly Scores"}
        }, {
            "$match": {
                "_id": emp_id
            }
        }]
        return dumps(Database.DATABASE[collection].aggregate(pipeline))

    @classmethod
    def get_emp_inspections(cls, emp_id):
        pipeline = [{
            "$match": {
                "_id": emp_id
                }
            }, {
            "$lookup": {
                'from': "ins_employees",
                'localField': "_id",
                'foreignField': "emp_id",
                'as': "empInspections"
                }
            },  {
           "$lookup": {
               'from': "inspections",
               'localField': "empInspections.ins_id",
               'foreignField': "_id",
               'as': "inspections"
           }
        }]
        return Database.DATABASE[collection].aggregate(pipeline)


    @classmethod
    def calculate_emp_monthly_avg(cls, emp_id, month, year, score, num_inspections):
        EmployeeMonthlyScore.update_monthly_score_and_num_inspections(emp_id, month,
                                                                      year, score, num_inspections)

    @classmethod
    def calculate_emp_avg(cls, emp_id, score_to_deduct, num_inspections_to_deduct):
        Database.DATABASE[collection].update({'_id': emp_id}, {'$inc': {'total_score': score_to_deduct,
                                                                        'num_inspections': num_inspections_to_deduct}})