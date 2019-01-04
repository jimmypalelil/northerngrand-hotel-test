from bson.json_util import dumps

from src.common.database import Database
from src.models.Inspection import createEmployees
from src.models.Inspection.employee import Employee
from src.models.Inspection.inspectionItem import InspectionItem
from src.models.Inspection.employeemonthlyscore import EmployeeMonthlyScore

Database.go()

def createInsItems():
    items = [["vent", "washroom"], ["tub/tile", "washroom"], ["sink", "washroom"], ["toilet bowl", "washroom"],
             ["towels", "washroom"], ["shower curtain / rod", "washroom"], ["ammenities", "washroom"],
             ["floor", "washroom"], ["mirror", "washroom"], ["counter/edges", "washroom"],
             ["closet blanket", "entrance"], ["iron", "entrance"], ["ironing board/cover", "entrance"],
             ["recylce bin", "entrance"], ["boot tray", "entrance"], ["main door ", "entrance"],
             ["tile/edges", "entrance"], ["coffee tray", "coffee station"], ["coffee ammenites", "coffee station"],
             ["coffee pods ", "coffee station"], ["keurig pot", "coffee station"], ["bed ", "front room"],
             ["pillows", "front room"], ["scarf", "front room"], ["note pad/pen", "front room"],
             ["namecard/chocolate", "front room"], ["heater/ac unit", "front room"], ["blind", "front room"],
             ["window ledge", "front room"], ["lampshade/base", "front room"], ["bed lamps", "front room"],
             ["chair", "front room"], ["dusting of furniture", "front room"], ["vaccuming", "front room"],
             ["mirror", "front room"], ["headboard ledge ", "front room"], ["icebucket/tray glasses", "front room"],
             ["picture frame/bench", "front room"], ["drawers", "front room"], ["overall appearance", "Miscellaneous"]]

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