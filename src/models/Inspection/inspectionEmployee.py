import uuid
from src.common.database import Database

collection = 'ins_employees'


class InspectionEmployee(object):
    def __init__(self, ins_id, emp_id, month, year, _id=None):
        self.ins_id = ins_id
        self.emp_id = emp_id
        self.month = month
        self.year = year
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "ins_id": self.ins_id,
            "emp_id": self.emp_id,
            "month": self.month,
            "year": self.year,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.update(collection, {"_id": self._id}, self.json())

    @classmethod
    def get_by_ins_id(cls, ins_id):
        return Database.find(collection, {"ins_id": ins_id})

    def insert(self):
        Database.insert(collection, self.json())

    @classmethod
    def remove_by_emp_id(cls, emp_id):
        Database.remove(collection, {"emp_id": emp_id})

    @classmethod
    def remove_by_ins_id_and_emp_id(cls, ins_id, emp_id):
        Database.remove(collection, {"ins_id": ins_id, 'emp_id': emp_id})

    @classmethod
    def remove_by_emp_id_month_year(cls, emp_id, month, year):
        Database.remove(collection, {'emp_id': emp_id, 'month': month, 'year': year})
