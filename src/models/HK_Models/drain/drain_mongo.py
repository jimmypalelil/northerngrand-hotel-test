# import uuid
# from bson.json_util import dumps
#
# from src.common.database import Database
#
# Database.go()
#
# rooms = list(Database.DATABASE['rooms'].find())
#
# monthTypes = [
#     ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'],
#     ['jan to jun', 'jul to dec'],
#     ['jan to mar', 'apr to jun', 'july to sep', 'oct to dec']
# ]
#
# types = [
#     # {"label": 'Bedding', "data": 'beddings', "index": 0},
#     # {"label": 'Carpet Shampoo', "data": 'carpets', "index": 1},
#     # {"label": 'Bed Flips', "data": 'mattress', "index": 2}, {"label": 'Pillows', "data": 'pillows', "index": 2},
#     # {"label": 'Pillow Protectors', "data": 'pillowss', "index": 1}, {"label": 'Drains', "data": 'drains', "index": 0},
#     # {"label": 'Wall Washing', "data": 'walls', "index": 2}, {"label": 'Doors', "data": 'doors', "index": 0},
#     # {"label": 'Toilet Knobs', "data": 'knobs', "index": 0},
#     {"label": 'Fridge/Microwave', "data": 'fridge', "index": 0},
#     {"label": 'Floor Hallways', "data": 'floorHallways', "index": 0}, {"label": 'Tile Grout', "data": 'grout', "index": 1},
#     {"label": 'Wall Washing Washrooms', "data": 'wallWashWashrooms', "index": 2}
# ]
#
# year = '2020'
# #
# # for type in types:
# #     index = type['index']
# #     collection = type['data']
# #     print(collection)
# #     monthArray = monthTypes[index]
# #     for room in rooms:
# #         for month in monthArray:
# #             print(room['room_number'], collection, month)
# #             Database.insert(collection, {
# #                 "room_number": room['room_number'],
# #                 "type": room['type'],
# #                 "month": month,
# #                 "year": year,
# #                 "status": 'not done',
# #                 "cat": collection,
# #                 "_id": uuid.uuid4().hex
# #             })
