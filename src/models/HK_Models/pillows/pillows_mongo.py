from src.common.database import Database
from src.models.HK_Models.pillows.pillows import Pillows
Database.go()

roooms = Database.DATABASE['rooms'].find()

months = ['jan to jun', 'jul to dec']

for rom in roooms:
    for month in months:
        Pillows(rom['room_number'], rom['type'], month, '2018', 'not done', 'pillowss', rom['_id']).insert()

# pillows_protectors = Database.DATABASE['pillowss'].find()
# for rom in pillows_protectors:
#     roms = Pillows.get_by_room_id('pillowss', rom['_id'])
#     roms.cat = "pillowss"
#     Database.update('pillowss', {"_id": roms._id}, roms.json())