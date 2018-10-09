import uuid
from src.common.database import Database


class Carpet(object):
    def __init__(self, room_number, type, month, year, status, cat, room_id, _id=None):
        self.room_number = room_number
        self.type = type
        self.month = month
        self.year = year
        self.status = status
        self.cat = cat
        self.room_id = room_id
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "room_number": self.room_number,
            "type": self.type,
            "month": self.month,
            "year": self.year,
            "status": self.status,
            "cat": self.cat,
            "room_id": self.room_id,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.update('carpets', {"_id": self._id}, self.json())

    @classmethod
    def get_by_room_id(cls, id):
        return cls(**Database.find_one('carpets', {"_id": id}))

    def insert(self):
        Database.insert('carpets', self.json())