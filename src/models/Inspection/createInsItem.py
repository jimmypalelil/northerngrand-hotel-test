from bson.json_util import dumps

from src.common.database import Database
from src.models.Inspection import createEmployees
from src.models.Inspection.employee import Employee
from src.models.Inspection.inspectionItem import InspectionItem
from src.models.Inspection.employeemonthlyscore import EmployeeMonthlyScore

Database.go()

def createInsItems():
    items = [["just checking ", "window"], ["all coffee pods in ", "coffee station"],
             ["sink", "washroom"], ["toilet bowl", "washroom"]]

    for item in items:
        InspectionItem(item[0], item[1]).insert()

# createInsItems()

def resetInspections():
    Database.DATABASE['ins_employees'].drop()
    Database.DATABASE['ins_monthly_scores'].drop()
    Database.DATABASE['inspections'].drop()
    Database.DATABASE['ins_scores'].drop()
    Database.DATABASE['employees'].drop()
    Database.DATABASE['ins_items'].drop()
    createEmployees.createEmployees()
    createInsItems()

# resetEmployees()


def get_ins_emps(ins_id):
    pipeline = [{
        "$match": {
            "_id": ins_id
        }
    }, {
        "$lookup": {
            'from': "ins_employees",
            'localField': "_id",
            'foreignField': "insId",
            'as': "ins_employees"
        }
    }, {
        "$unwind": "$ins_employees"
    }, {
        "$project": {
            "employees": "$ins_employees"
        }
    }]
    return Database.DATABASE['inspections'].aggregate(pipeline)


def get_emp_inspections(emp_id):
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
    return Database.DATABASE['employees'].aggregate(pipeline)


emps = get_emp_inspections('efadbd4583574f87b1ec35a4c926257b')

for emp in emps:
    print(emp)