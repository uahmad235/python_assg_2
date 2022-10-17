from pymongo import MongoClient


class MongoDBClient:
    def __init__(self, db: str) -> None:
        self.client = MongoClient('mongodb://mongodb:27017')
        self.db = self.client[db]
