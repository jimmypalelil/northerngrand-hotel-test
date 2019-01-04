from src.common.database import Database
from src.models.HK_Models.bedding.bedding import Bedding
from src.models.HK_Models.carpet_shampoo.carpet_shampoo import Carpet
from src.models.HK_Models.mattress.mattress import Mattress
from src.models.HK_Models.pillow_protector.pillow_protector import Pillow
from src.models.HK_Models.pillows.pillows import Pillows

Database.go()

rooms = Database.DATABASE['rooms'].find()

# # Beddings
# months = ['jan', 'feb', 'mar', 'apr','may','jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
# for room in rooms:
#     for month in months:
#         Bedding(room['room_number'], room['type'], month, '2019', 'not done','beddings', room['_id']).insert()
#
# # Carpet Shampoo
# months = ['jan to jun', 'jul to dec']
# for room in rooms:
#     for month in months:
#         Carpet(room['room_number'], room['type'], month, '2019', 'not done', 'carpets', room['_id']).insert()
#         Pillows(room['room_number'], room['type'], month, '2019', 'not done', 'pillowss', room['_id']).insert()

# Bed Flips
months = ['jan to mar', 'apr to jun', 'july to sep', 'oct to dec']
for room in rooms:
    for month in months:
        Mattress(room['room_number'], room['type'], month, '2019', 'not done', 'mattress', room['_id']).insert()
        Pillow(room['room_number'], room['type'], month, '2019', 'not done', 'pillows', room['_id']).insert()

# # Pillow Protectors
# months = ['jan to mar', 'apr to jun', 'july to sep', 'oct to dec']
# for room in rooms:
#     for month in months:
#         Pillow(room['room_number'], room['type'], month, '2019', 'not done', 'pillows', room['_id']).insert()

# # Pillows
# months = ['jan to jun', 'jul to dec']
# for room in rooms:
#     for month in months:
#         Pillows(room['room_number'], room['type'], month, '2019', 'not done', 'pillowss', room['_id']).insert()
