from bson.json_util import dumps

from src.common.database import Database
from src.models.Inspection import createEmployees
from src.models.Inspection.inspectionItem import InspectionItem


Database.go()


def create_ins_items():
    items = [["fridge ", "front room"], ["microwave", "front room"], ["drawers menu", "front room"]]

    for item in items:
        InspectionItem.insert(item[0], item[1])


def reset_inspections():
    Database.DATABASE['ins_employees'].drop()
    Database.DATABASE['ins_monthly_scores'].drop()
    Database.DATABASE['inspections'].drop()
    Database.DATABASE['ins_scores'].drop()
    Database.DATABASE['employees'].drop()
    createEmployees.createEmployees()
    create_ins_items()


def get_inspections_for_employee(emp_id, month, year):
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
    }, {
        "$unwind": "$empInspections"
    }, {
        "$match": {
            "empInspections.month": month,
            "empInspections.year": year
        }
    }, {
        "$lookup": {
            'from': "inspections",
            'localField': "empInspections.ins_id",
            'foreignField': "_id",
            'as': "inspections"
        }
    }, {
       "$match": {
           "inspections.num_employees": 1
       }
    }, {
        "$unwind": "$inspections"
    }, {
        "$project": {
            "inspections": "$inspections._id"
        }
    }]
    print(dumps(Database.DATABASE['employees'].aggregate(pipeline)))
    return Database.DATABASE['employees'].aggregate(pipeline)


# get_inspections_for_employee('3abbecbbe13a45ed9b8b5453a09b281c', 'jan', 2019)
