import uuid

from src.common.database import Database


class Item(object):
    def __init__(self, room_number, item_description, date, cat=None, _id=None):
        self.room_number = room_number
        self.item_description = item_description
        self.date = date
        self.cat = 'losts' if cat is None else cat
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "room_number": self.room_number,
            "item_description": self.item_description,
            "date": self.date,
            "cat": self.cat,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.update('losts', {"_id": self._id}, self.json())

    @classmethod
    def get_by_room_id(cls, id):
        return cls(**Database.find_one('losts', {"_id": id}))

    def insert(self):
        Database.insert('losts', self.json())

    def remove(self, id):
        Database.remove('losts', {"_id": id})

    def update(self, id, data):
        Database.update('losts', {"_id": id}, data)