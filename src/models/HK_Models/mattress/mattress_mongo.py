from src.common.database import Database
from src.models.HK_Models.mattress.mattress import Mattress
Database.go()

roooms = Database.DATABASE['rooms'].find()

months = ['jan to mar', 'apr to jun', 'july to sep','oct to dec']


for rom in roooms:
    for month in months:
        Mattress(rom['room_number'], rom['type'], month, '2018', 'not done','mattress', rom['_id']).insert()