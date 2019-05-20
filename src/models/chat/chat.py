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
            "date": self.date
        }

    @staticmethod
    def get_all_chats():
        return dumps(Database.findAll(collection))

    @staticmethod
    def get_chats_by_number(n):
        return Database.DATABASE[collection].aggregate([{'$sort': {'date': -1}}, {'$limit': n}])

    @staticmethod
    def check_for_duplicate(email,password):
        search_result = Database.find_one('users', {'email': email, 'password': password})
        if search_result is not None:
            return True
        else:
            return False

    @staticmethod
    def is_login_valid(email, password):
        search_result = Database.find_one('users', {'email': email, "password": password})
        if search_result is not None:
            return True
        else:
            return False

    @classmethod
    def return_chat_for_email(cls, email):
        return cls(**Database.find_one('users', {'email': email}))

    @staticmethod
    def remove_admin_chat():
        Database.remove(collection, {'from': 'jimmypalelil@gmail.com'})
