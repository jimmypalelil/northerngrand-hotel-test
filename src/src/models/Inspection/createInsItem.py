from bson.json_util import dumps

from src.common.database import Database
from src.models.Inspection import createEmployees
from src.models.Inspection.employee import Employee
from src.models.Inspection.inspectionItem import InspectionItem
from src.models.Inspection.score import Score

Database.go()

def createInsItems():
    items = [["just checking ", "window"], ["all coffee pods in ", "coffee station"],
             ["sink", "washroom"], ["toilet bowl", "washroom"]]

    for item in items:
        InspectionItem(item[0], item[1]).insert()

# createInsItems()

def resetInspections():
    emps = Database.findAll('employees')
    for emp in emps:
        tempEmployee = Employee(**emp)
        tempEmployee.avg_score = 0
        tempEmployee.num_inspections = 0
        tempEmployee.update()

    Database.DATABASE['ins_employees'].drop()
    Database.DATABASE['ins_monthly_scores'].drop()
    Database.DATABASE['inspections'].drop()
    Database.DATABASE['ins_scores'].drop()
    Database.DATABASE['employees'].drop()
    Database.DATABASE['ins_items'].drop()
    createEmployees.createEmployees()
    createInsItems()

# resetEmployees()
