import sys
import os
import csv

sys.path.append("..")
from json_utils import insert_data
from database_utils import connect_to_mongo

with connect_to_mongo("test", "jobs") as collection:
    with open("task_2_item.csv", "r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=";")
        data_list = list(csv_reader)
    # collection.insert_many(data_list)

    # вывод минимальной, средней, максимальной salary
    pipeline1 = [
        {
            "$group": {
                "_id": None,
                "min_salary": {"$min": "$salary"},
                "avg_salary": {"$avg": "$salary"},
                "max_salary": {"$max": "$salary"},
            }
        }
    ]
    result1 = list(collection.aggregate(pipeline1))

    # вывод количества данных по представленным профессиям
    pipeline2 = [{"$group": {"_id": "$job", "count": {"$count": {}}}}]
    result2 = list(collection.aggregate(pipeline2))

    # вывод минимальной, средней, максимальной salary по городу
    pipeline3 = [
        {
            "$group": {
                "_id": "$city",
                "min_salary": {"$min": "$salary"},
                "avg_salary": {"$avg": "$salary"},
                "max_salary": {"$max": "$salary"},
            }
        }
    ]
    result3 = list(collection.aggregate(pipeline3))

    # вывод минимальной, средней, максимальной salary по профессии
    pipeline4 = [
        {
            "$group": {
                "_id": "$job",
                "min_salary": {"$min": "$salary"},
                "avg_salary": {"$avg": "$salary"},
                "max_salary": {"$max": "$salary"},
            }
        }
    ]
    result4 = list(collection.aggregate(pipeline4))

    # вывод минимального, среднего, максимального возраста по городу
    pipeline5 = [
        {
            "$group": {
                "_id": "$city",
                "min_age": {"$min": "$age"},
                "avg_age": {"$avg": "$age"},
                "max_age": {"$max": "$age"},
            }
        }
    ]
    result5 = list(collection.aggregate(pipeline5))

    # вывод минимального, среднего, максимального возраста по профессии
    pipeline6 = [
        {
            "$group": {
                "_id": "$job",
                "min_age": {"$min": "$age"},
                "avg_age": {"$avg": "$age"},
                "max_age": {"$max": "$age"},
            }
        }
    ]
    result6 = list(collection.aggregate(pipeline6))

    # вывод максимальной заработной платы при минимальном возрасте
    pipeline7 = [
        {"$group": {"_id": "$age", "max_salary": {"$max": "$salary"}}},
        {"$sort": {"_id": 1}},
        {"$limit": 1},
    ]
    result7 = list(collection.aggregate(pipeline7))

    # вывод минимальной заработной платы при максимальной возрасте
    pipeline8 = [
        {"$group": {"_id": "$age", "min_salary": {"$min": "$salary"}}},
        {"$sort": {"_id": -1}},
        {"$limit": 1},
    ]
    result8 = list(collection.aggregate(pipeline8))

    # вывод минимального, среднего, максимального возраста по городу, при условии, что заработная плата больше 50 000, отсортировать вывод по любому полю.
    pipeline9 = [
        {"$match": {"salary": {"$gt": 50000}}},
        {
            "$group": {
                "_id": "$city",
                "min_age": {"$min": "$age"},
                "avg_age": {"$avg": "$age"},
                "max_age": {"$max": "$age"},
            }
        },
        {"$sort": {"avg_age": 1}},
    ]
    result9 = list(collection.aggregate(pipeline9))

    # вывод минимальной, средней, максимальной salary в произвольно заданных диапазонах по городу, профессии, и возрасту: 18<age<25 & 50<age<65
    pipeline10 = [
        {
            "$match": {
                "$and": [
                    {"salary": {"$gt": 50000}},
                    {
                        "$or": [
                            {"age": {"$gt": 18, "$lt": 25}},
                            {"age": {"$gt": 50, "$lt": 65}},
                        ]
                    },
                ]
            }
        },
        {
            "$group": {
                "_id": {"city": "$city", "job": "$job"},
                "min_salary": {"$min": "$salary"},
                "avg_salary": {"$avg": "$salary"},
                "max_salary": {"$max": "$salary"},
            }
        },
    ]
    result10 = list(collection.aggregate(pipeline10))

    # произвольный запрос с $match, $group, $sort
    pipeline11 = [
        {"$match": {"city": "Семана", "job": "Программист", "age": {"$gt": 30}}},
        {"$group": {"_id": "$city", "avg_salary": {"$avg": "$salary"}}},
        {"$sort": {"avg_salary": -1}},
    ]
    result11 = list(collection.aggregate(pipeline11))

    os.makedirs("results", exist_ok=True)
    insert_data(os.path.join("results", "result1.json"), result1)
    insert_data(os.path.join("results", "result2.json"), result2)
    insert_data(os.path.join("results", "result3.json"), result3)
    insert_data(os.path.join("results", "result4.json"), result4)
    insert_data(os.path.join("results", "result5.json"), result5)
    insert_data(os.path.join("results", "result6.json"), result6)
    insert_data(os.path.join("results", "result7.json"), result7)
    insert_data(os.path.join("results", "result8.json"), result8)
    insert_data(os.path.join("results", "result9.json"), result9)
    insert_data(os.path.join("results", "result10.json"), result10)
    insert_data(os.path.join("results", "result11.json"), result11)
