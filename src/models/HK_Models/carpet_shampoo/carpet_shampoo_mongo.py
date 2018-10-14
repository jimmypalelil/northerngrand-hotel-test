from src.common.database import Database
from src.models.HK_Models.carpet_shampoo import Carpet
Database.go()

roooms = Database.DATABASE['rooms'].find()



months = ['jan to jun', 'jul to dec']


for rom in roooms:
    for month in months:
        Carpet(rom['room_number'], rom['type'], month, '2018', 'not done', 'carpets', rom['_id']).insert()