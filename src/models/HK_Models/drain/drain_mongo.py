from src.common.database import Database
from src.models.HK_Models.drain.drain import Drain
from src.models.HK_Models.wallwashing.wallwashing import WallWashing

Database.go()

rooms = Database.DATABASE['rooms'].find()

monthly = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
quarterly = ['jan to mar', 'apr to jun', 'july to sep', 'oct to dec']
for room in rooms:
    for month in monthly:
        Drain(room['room_number'], room['type'], month, '2019', 'not done', 'drains', room['_id']).insert()
    for month in quarterly:
        WallWashing(room['room_number'], room['type'], month, '2019', 'not done', 'walls', room['_id']).insert()
