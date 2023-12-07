import pymongo
import sys
import json
import os

sys.path.append("..")
from json_utils import insert_data
from database_utils import connect_to_mongo

with connect_to_mongo('test', 'jobs') as collection:

    with open("task_1_item.json", "r") as file:
        data = json.load(file)

    collection.insert_many(data)
    
    query1 = {}
    result1 = list(collection.find(query1, limit=15))

    query2 = {"age": {"$lt": 30}}
    result2 = list(collection.find(query2, limit=15).sort("salary", pymongo.DESCENDING))

    query3 = {
        "city": "Фигерас",
        "job": {"$in": ["Строитель", "Строитель", "Строитель"]},
    }
    result3 = list(collection.find(query1).limit(10).sort("age", pymongo.ASCENDING))

    query4 = {
        "age": {"$gte": 25, "$lte": 35},
        "year": {"$in": [2019, 2022]},
        "$or": [
            {"salary": {"$gt": 50000, "$lte": 75000}},
            {"salary": {"$gt": 125000, "$lt": 150000}},
        ],
    }
    result4 = collection.count_documents(query4)


    os.makedirs("results", exist_ok=True)

    insert_data(os.path.join("results", "result1.json"), result1)
    insert_data(os.path.join("results", "result2.json"), result2)
    insert_data(os.path.join("results", "result3.json"), result3)
    insert_data(os.path.join("results", "result4.json"), result4)
