from src.common.database import Database
from src.models.HK_Models.pillow_protector.pillow_protector import Pillow
Database.go()

roooms = Database.DATABASE['rooms'].find()

months = ['jan to mar', 'apr to jun', 'july to sep', 'oct to dec']


for rom in roooms:
    for month in months:
        Pillow(rom['room_number'], rom['type'], month, '2018', 'not done', 'pillows', rom['_id']).insert()
        print(rom)