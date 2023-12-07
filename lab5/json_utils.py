import json
import pymongo
from bson import ObjectId


class MongoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


def insert_data(filename, data):
    with open(filename, "w") as r_json:
        json.dump(
            data,
            r_json,
            cls=MongoEncoder,
            indent=2,
            ensure_ascii=False,
        )
