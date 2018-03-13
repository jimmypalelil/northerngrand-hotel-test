import pymongo
import os


class Database(object):
    # URI = os.environ.get('MONGODB_URI')

    #original database
    #URI = 'mongodb://jimmypalelil:ahaaha@ds249707.mlab.com:49707/heroku_btv18l4k'

    # test Database
    URI = 'mongodb://jimmyavenged:9830100avenue@ds233228.mlab.com:33228/awsdb'

    DATABASE = None

    @staticmethod
    def go():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client.get_default_database()

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def update(collection,query, data):
        Database.DATABASE[collection].update(query, data, upsert=False)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)