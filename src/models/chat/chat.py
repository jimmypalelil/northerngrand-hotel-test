import uuid
from json import dumps
from src.common.database import Database

collection = 'chats'


class Chat(object):
    def __init__(self, to_email, from_email, msg, date, _id=None):
        self.to_email = to_email
        self.from_email = from_email
        self.msg = msg
        self.date = date
        self._id = uuid.uuid4().hex if _id is None else _id

    @staticmethod
    def save_to_mongo(to_email, from_email, msg, date):
        Chat(to_email, from_email, msg, date).insert_chat()

    def insert_chat(self):
        return Database.insert(collection, self.json())

    def json(self):
        return {
            "to_email": self.to_email,
            "from_email": self.from_email,
            "msg": self.msg,
            "date": self.date,
            "_id": self._id
        }

    @staticmethod
    def get_all_chats():
        return dumps(Database.findAll(collection))

    @staticmethod
    def get_chats_by_number(n):
        return Database.DATABASE[collection].aggregate([{'$sort': {'date': -1}}, {'$limit': n}])

    @classmethod
    def remove_msg(cls, id):
        Database.remove('chats', {'_id': id})
