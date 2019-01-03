from src.common.database import Database
from src.models.Inspection.employee import Employee
Database.go()

def createEmployees():
    names = ['Ruth K', 'Mary', 'Sharon', 'Bonny', 'Sunil', 'Pardeep', 'Harvinder']

    for name in names:
        Employee(name,0,0,0).insert()
