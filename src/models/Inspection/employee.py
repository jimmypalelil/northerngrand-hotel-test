import uuid

from bson.json_util import dumps
from src.common.database import Database
from src.models.Inspection.score import Score

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

    @classmethod
    def updateEmployeeScore(cls, empId, avg_score, count):
        emp = Employee.get_by_id(empId)
        emp.avg_score = avg_score
        emp.num_inspections = count
        Database.update(collection, {"_id": empId}, emp.json())

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


    @classmethod
    def calculateMonthlyAvg(cls, empID, month, year):
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
        }, {
            "$lookup": {
                'from': "inspections",
                'localField': "empInspections.insId",
                'foreignField': "_id",
                'as': "inspections"
            }
        }, {
            "$unwind": "$inspections"
        }, {
            "$match": {
                "inspections.month": month,
                "inspections.year": year
            }
        }, {
            "$project": {
                "inspections": "$inspections"
            }
        }]
        empMonthlyIns = Database.DATABASE['employees'].aggregate(pipeline)
        totalscore = 0
        count = 0
        for ins in empMonthlyIns:
            score = ins['inspections']['score']
            totalscore += score
            count += 1
        if count == 0:
            Score.remove_by_empId_and_month(empID, month)
        else:
            avgScore = totalscore / count
            empScore = Score(**Score.get_by_emp_id(empID, month))
            empScore.score = avgScore
            empScore.num_inspections = empScore.num_inspections - 1
            Score.updateScore(empID, month, year, empScore.json())

    @classmethod
    def calculateAllAvg(cls, empID):
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
        }, {
            "$lookup": {
                'from': "inspections",
                'localField': "empInspections.insId",
                'foreignField': "_id",
                'as': "inspections"
            }
        }, {
            "$unwind": "$inspections"
        }, {
            "$project": {
                "inspections": "$inspections"
            }
        }]
        empsIns = Database.DATABASE['employees'].aggregate(pipeline)
        totalscore = 0
        count = 0
        for ins in empsIns:
            score = ins['inspections']['score']
            totalscore += score
            count += 1
        if count == 0:
            Employee.updateEmployeeScore(empID, 0, 0)
        else:
            avg_score = totalscore / count
            Employee.updateEmployeeScore(empID, avg_score, count)


    @classmethod
    def calculateAvgForAllEmployees(cls, month, year):
        emps = Database.findAll(collection)
        for emp in emps:
            Employee.calculateMonthlyAvg(emp['_id'],month, year)
            Employee.calculateAllAvg(emp['_id'])