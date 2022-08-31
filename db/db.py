import pymongo
from dotenv import dotenv_values
config = dotenv_values('.env')


class Db:
    def __init__(self):

        self.client = pymongo.MongoClient(config['DB_URL'])
        self.db = self.client[config['DB_NAME']]

    def collection(self, name):
        return self.db.get_collection(name)
    