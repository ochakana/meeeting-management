from json import loads

from bson.json_util import dumps
from pymongo import MongoClient


class MongoDBClient:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client.get_database()

    def get_last_record_number(self, collection_name):
        last_record = self.db[collection_name].find_one(sort=[("recordNumber", -1)])
        return last_record["recordNumber"] if last_record else 0

    def insert_data(self, collection_name, data):
        # 既存のドキュメントと重複していないか確認
        if not self.db[collection_name].find_one(data):
            last_record_number = self.get_last_record_number(collection_name)
            data["recordNumber"] = last_record_number + 1
            self.db[collection_name].insert_one(data)

    def get_data(self, collection_name, record_id=None):
        collection = self.db[collection_name]
        if record_id is not None:
            data = collection.find_one({"recordNumber": record_id})
            return data if data else None
        else:
            data = list(collection.find({}))
            return data

    def update_data(self, collection_name, record_id, data):
        self.db[collection_name].update_one(
            {"recordNumber": int(record_id)}, {"$set": data}
        )

    def delete_data(self, collection_name, record_id=None, category_names=None):
        if record_id is not None:
            self.db[collection_name].delete_one({"recordNumber": int(record_id)})
        elif category_names is not None:
            self.db[collection_name].delete_many({"category": {"$in": category_names}})

