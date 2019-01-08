from src.common.database import Database
from src.models.Inspection import createEmployees
from src.models.Inspection.inspectionItem import InspectionItem


Database.go()


def create_ins_items():
    items = [["fridge ", "front room"], ["micowave", "front room"], ["drawers menu", "front room"]]

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
