import uuid

from bson.json_util import dumps
from src.common.database import Database

collection = 'inspections'

class Inspection(object):
    def __init__(self, room_number, day, month, year, score, num_employees, _id=None):
        self.room_number = room_number
        self.day = day
        self.month = month
        self.year = year
        self.score = score
        self.num_employees = num_employees
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "room_number": self.room_number,
            "month": self.month,
            "day": self.day,
            "year": self.year,
            "score": self.score,
            "num_employees": self.num_employees,
            "_id": self._id
        }

    def updateSelf(self):
        Database.update(collection, {"_id": self._id}, self.json())

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(collection, {"_id": id}))

    @classmethod
    def get_by_month_and_year(cls, month, year):
        return Database.find(collection, {"month": month, "year": year})

    @classmethod
    def set_ins_score(cls, ins_id, score):
        Database.DATABASE[collection].update({'_id': ins_id}, {'$set': {'score': score}})

    def insert(self):
        Database.insert(collection, self.json())

    @classmethod
    def remove(cls, id):
        Database.remove(collection, {"_id": id})\

    @classmethod
    def remove_by_month_and_year(cls, month, year):
        inspections = Inspection.get_by_month_and_year(month, year)
        for ins in inspections:
            if ins['num_employees'] == 1:
                Database.remove(collection, {"month": month, "year": year})

    @classmethod
    def update(cls, id, data):
        Database.update(collection, {"_id": id}, data)

    def insert_one(self):
        return Database.insertOne(collection, self.json())

    @classmethod
    def get_inspection_items(cls, ins_id, emp_id):
        pipeline = [{
            "$match": {
                "_id": ins_id
            }
        }, {
            "$lookup": {
                'from': "ins_scores",
                'localField': "_id",
                'foreignField': "ins_id",
                'as': "item"
            }
        }, {
            "$unwind": "$item"
        }, {
           "$match": {
               "item.emp_id": emp_id
           }
        }, {
            "$lookup": {
                'from': "ins_items",
                'localField': "item.item_id",
                'foreignField': "_id",
                'as': "inspection"
            }
        }, {
            "$unwind": "$inspection"
        }, {
            "$group": {
                "_id": "$inspection.cat",
                "items": {"$push": "$$ROOT"}
            }
        }]
        return dumps(Database.DATABASE[collection].aggregate(pipeline))


    @classmethod
    def get_ins_emp_count(cls, ins_id):
        pipeline = [{
            "$match": {
                "_id": ins_id
            }
        }, {
            "$lookup": {
                'from': "ins_employees",
                'localField': "_id",
                'foreignField': "ins_id",
                'as': "ins_employees"
            }
        }, {
            "$unwind": "$ins_employees"
        }, {
            "$group": {
                "_id": None,
                "total": {"$sum": 1},
                "emps": {"$push": "$$ROOT"}
            }
        }]
        return Database.DATABASE[collection].aggregate(pipeline)

    @classmethod
    def get_ins_emps(cls, ins_id):
        pipeline = [{
            "$match": {
                "_id": ins_id
            }
        }, {
            "$lookup": {
                'from': "ins_employees",
                'localField': "_id",
                'foreignField': "ins_id",
                'as': "ins_employees"
            }
        }, {
            "$unwind": "$ins_employees"
        }]
        return Database.DATABASE[collection].aggregate(pipeline)

    @classmethod
    def set_num_emps(cls, ins_id, num_employees):
        Database.DATABASE[collection].update({'_id': ins_id}, {'$inc': {'num_employees': num_employees}})

