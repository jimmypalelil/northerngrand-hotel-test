from src.common.database import Database
from src.models.HK_Models.bedding.bedding import Bedding
Database.go()

roooms = Database.DATABASE['rooms'].find()

months = ['jan', 'feb', 'mar', 'apr','may','jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']


for rom in roooms:
    for month in months:
        Bedding(rom['room_number'], rom['type'], month, '2018', 'not done','beddings', rom['_id']).insert()