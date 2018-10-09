from src.models.room.room import room
from src.common.database import Database
from src.models.bedding.bedding import Bedding
Database.go()

roooms = Database.DATABASE['rooms'].find()

months = ['jan', 'feb', 'mar', 'apr','may','jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

def run():
    for rom in roooms:
        for month in months:
            Bedding(rom['room_number'], rom['type'], month, '2018', 'not done','beddings', rom['_id']).insert()