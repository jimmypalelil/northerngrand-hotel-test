import uuid
from bson.json_util import dumps
from src.common.database import Database

collection = 'ins_monthly_scores'


class EmployeeMonthlyScore(object):
    def __init__(self, emp_id, month, year, score, num_inspections=None, _id=None):
        self.emp_id = emp_id
        self.month = month
        self.year = year
        self.score = score
        self.total_score = score
        self.num_inspections = 1 if num_inspections is None else num_inspections
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "emp_id": self.emp_id,
            "month": self.month,
            "year": self.year,
            "num_inspections": self.num_inspections,
            "score": self.score,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.update(collection, {"_id": self._id}, self.json())

    @classmethod
    def get_by_emp_id_month_year(cls, emp_id, month, year):
        return Database.find_one(collection, {"emp_id": emp_id, "month": month, "year": year})

    def insert(self):
        Database.insert(collection, self.json())

    @classmethod
    def remove(cls, id):
        Database.remove(collection, {"_id": id})

    @classmethod
    def remove_by_emp_id_and_month_and_year(cls, emp_id, month, year):
        Database.remove(collection, {"emp_id": emp_id, "month": month, "year": year})

    @classmethod
    def remove_by_month_and_year(cls, month, year):
        Database.remove(collection, {"month": month, "year": year})

    @classmethod
    def updateScore(cls, emp_id, month, year, data):
        Database.update(collection, {"emp_id": emp_id, "month": month, "year": year}, data)

    @staticmethod
    def getAllEmployees():
        return dumps(Database.findAll(collection))

    @classmethod
    def update_monthly_score_and_num_inspections(cls, emp_id, month, year, score, num_inspections):
        Database.DATABASE[collection].update({"emp_id": emp_id, "month": month, "year": year},
                                             {'$inc': {'num_inspections': num_inspections, 'score': score}})
        num_inspections = EmployeeMonthlyScore.get_by_emp_id_month_year(emp_id, month, year)['num_inspections']
        if num_inspections == 0:
            EmployeeMonthlyScore.remove_by_emp_id_and_month_and_year(emp_id, month, year)
