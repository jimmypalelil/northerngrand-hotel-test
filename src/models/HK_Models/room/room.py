import uuid
from src.common.database import Database

class room(object):
    def __init__(self, room_number, type, _id = None):
        self.room_number = room_number
        self.type = type
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "room_number": self.room_number,
            "type": self.type,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert('rooms', self.json())

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one('rooms', {"_id": id}))


    def update(self, id):
        Database.update('rooms', {'_id': id}, self.json())