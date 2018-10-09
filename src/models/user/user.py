from flask import session
from src.common.database import Database

class User(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password

    @staticmethod
    def user_to_mongo(email, password):
        Database.DATABASE['users'].insert({'email': email, 'password': password})


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
    def return_user(cls, email):
        return cls(**Database.find_one('users', {'email': email}))

    @classmethod
    def logoutAll(cls):
        session['email'] = None