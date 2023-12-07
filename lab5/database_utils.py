import pymongo
from pymongo import MongoClient
from contextlib import contextmanager

uri = "mongodb+srv://capybara:capybara@cluster0.gubo8ho.mongodb.net/?retryWrites=true&w=majority"

@contextmanager
def connect_to_mongo(db_name, collection_name):
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]

    try:
        yield collection
    finally:
        client.close()
