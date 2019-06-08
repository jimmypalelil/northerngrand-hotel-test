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


def copy_data(from_uri, collection_to_copy):
    db = Database.getDatabase(from_uri)
    items = db[collection_to_copy].find()
    # Database.DATABASE[collection_to_copy].drop()
    for item in items:
        Database.DATABASE[collection_to_copy].insert(item)


def get_chats_by_skips(count):
    skip_count = int(count) + 50
    print(skip_count)
    data = Database.DATABASE['chats'].aggregate([{'$sort': {'date': -1}}, {'$skip': skip_count}, {'$limit': 50}])
    print(dumps(data))
