from src.common.database import Database
from src.models.Inspection import createEmployees
from src.models.Inspection.inspectionItem import InspectionItem


Database.go()


def create_ins_items():
    Database.DATABASE['ins_items'].drop()

    items = [["vent", "washroom"], ["tub/tile", "washroom"], ["sink", "washroom"], ["toilet bowl", "washroom"],
             ["towels", "washroom"], ["shower curtain / rod", "washroom"], ["amenities", "washroom"],
             ["floor", "washroom"], ["mirror", "washroom"], ["counter/edges", "washroom"],
             ["closet blanket", "entrance"], ["iron", "entrance"], ["ironing board/cover", "entrance"],
             ["recycle bin", "entrance"], ["boot tray", "entrance"], ["main door ", "entrance"],
             ["tile/edges", "entrance"], ["coffee tray", "coffee station"], ["coffee amenities", "coffee station"],
             ["coffee pods ", "coffee station"], ["keurig pot", "coffee station"], ["bed ", "front room"],
             ["pillows", "front room"], ["scarf", "front room"], ["note pad/pen", "front room"],
             ["namecard/chocolate", "front room"], ["heater/ac unit", "front room"], ["blind", "front room"],
             ["window ledge", "front room"], ["lampshade/base", "front room"], ["bed lamps", "front room"],
             ["chair", "front room"], ["dusting of furniture", "front room"], ["vacuuming", "front room"],
             ["mirror", "front room"], ["headboard ledge ", "front room"], ["icebucket/tray glasses", "front room"],
             ["picture frame/bench", "front room"], ["drawers", "front room"], ["overall appearance", "Miscellaneous"]]

    for item in items:
        InspectionItem(item[0], item[1]).save_to_mongo()

create_ins_items()


def reset_inspections():
    Database.DATABASE['ins_employees'].drop()
    Database.DATABASE['ins_monthly_scores'].drop()
    Database.DATABASE['inspections'].drop()
    Database.DATABASE['ins_scores'].drop()
    Database.DATABASE['employees'].drop()
    createEmployees.createEmployees()
    create_ins_items()
