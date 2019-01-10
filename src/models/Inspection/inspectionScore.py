import uuid

from bson.json_util import dumps
from src.common.database import Database

collection = 'ins_scores'


class InspectionScore(object):
    def __init__(self, ins_id, item_id, month, year, score, comment, _id=None):
        self.ins_id = ins_id
        self.item_id = item_id
        self.month = month
        self.year = year
        self.score = score
        self.comment = comment
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "ins_id": self.ins_id,
            "item_id": self.item_id,
            "month": self.month,
            "year": self.year,
            "score": self.score,
            "comment": self.comment,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.update(collection, {"_id": self._id}, self.json())

    def insert(self):
        Database.insert(collection, self.json())

    @classmethod
    def remove(cls, _id):
        Database.remove(collection, {"_id": _id})

    @classmethod
    def remove_by_ins_id(cls, ins_id):
        Database.remove(collection, {"ins_id": ins_id})

    @classmethod
    def remove_by_ins_id_emp_id(cls, ins_id, emp_id):
        Database.remove(collection, {"ins_id": ins_id, "emp_id": emp_id})

    @classmethod
    def remove_by_emp_id(cls, emp_id):
        Database.remove(collection, {"emp_id": emp_id})

    @classmethod
    def remove_by_emp_id_month_year(cls, emp_id, month, year):
        Database.remove(collection, {"emp_id": emp_id, "month": month, "year": year})
