import logging
import json
from pymongo import MongoClient

class MongoHandler(logging.Handler):
    def __init__(self, uri: str, db: str = "logsdb", collection: str = "logs"):
        super().__init__()
        self.client = MongoClient(uri)
        self.collection = self.client[db][collection]

    def emit(self, record):
        try:
            log_entry = self.format(record)
            log_data = json.loads(log_entry)
            self.collection.insert_one(log_data)
        except Exception as e:
            print(f"[MongoHandler ERROR] {e}")
