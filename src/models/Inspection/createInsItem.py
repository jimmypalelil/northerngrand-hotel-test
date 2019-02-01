from bson.json_util import dumps

from src.common.database import Database
from src.models.Inspection import createEmployees
from src.models.Inspection.inspectionItem import InspectionItem


Database.go()


def create_ins_items():
    items = [["laundry bag", "entrance"]]

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


def get_inspection_items(ins_id):
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
    return_data = Database.DATABASE['inspections'].aggregate(pipeline)
    for data in return_data:
        print(data)
    return return_data


# get_inspection_items('3a086c63f9324b45b9c55a05a97329df')