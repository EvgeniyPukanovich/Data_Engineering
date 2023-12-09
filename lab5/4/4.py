import os
import sys
import csv
import json

import pymongo

sys.path.append("..")
from json_utils import insert_data
from database_utils import connect_to_mongo

# Popular Baby Names by Sex and Ethnic Group Data were collected through civil birth registration in New York
# Year of Birth,Gender,Ethnicity,Child's First Name,Count,Rank


def insertData(collection):
    with open("Popular_Baby_Names_Male.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        collection.insert_many(data)

    with open("Popular_Baby_Names_Female.csv", "r", encoding="utf-8") as file:
        data = csv.DictReader(file)
        data_list = []
        for row in data:
            row["Year of Birth"] = int(row["Year of Birth"])
            row["Count"] = int(row["Count"])
            row["Rank"] = int(row["Rank"])
            data_list.append(row)
        collection.insert_many(data_list)


# замечено, что в датасете встречаются дубликаты
# таким образом удаляем дубликаты из коллекции
def insert_without_dups():
    with connect_to_mongo("test", "babies_dup") as collection:
        insertData(collection)

        # Specify the fields to consider for distinctness
        distinct_fields = [
            "Year of Birth",
            "Gender",
            "Ethnicity",
            "Child's First Name",
            "Count",
            "Rank",
        ]

        d = {field: f"$_id.{field}" for field in distinct_fields}
        d["_id"] = 0
        # Create an aggregation pipeline to group and keep only one document from each group
        pipeline = [
            {"$group": {"_id": {field: f"${field}" for field in distinct_fields}}},
            {"$project": d},
            {"$out": "babies"},
        ]
        collection.aggregate(pipeline)


with connect_to_mongo("test", "babies") as collection:
    # insert_without_dups()
    # первыe 10 записей, отсортированных по возрастанию по полю Rank;
    query1 = {}
    result1 = list(collection.find(query1, limit=10).sort("Rank", pymongo.ASCENDING))

    # первых 15 записей, отфильтрованных по предикату Count < 30 и отсортированных по убыванию по полю Rank
    query2 = {"Count": {"$lt": 30}}
    result2 = list(collection.find(query2, limit=15).sort("Rank", pymongo.DESCENDING))

    # популярность имен белых девочек
    query3 = {
        "Gender": "FEMALE",
        "Ethnicity": {"$regex": f".*WHITE.*", "$options": "i"},
    }
    result3 = list(collection.find(query3, limit=10).sort("Rank", pymongo.ASCENDING))

    # количество записей, получаемых в результате следующей фильтрации
    # (Rank от 20 до 30, year в [2010,2011], 10 < Count <= 20 || 40 < Count < 50 ).
    query4 = {
        "Rank": {"$gte": 20, "$lte": 30},
        "Year of Birth": {"$in": [2010, 2011]},
        "$or": [
            {"Count": {"$gt": 10, "$lte": 20}},
            {"Count": {"$gt": 40, "$lt": 50}},
        ],
    }
    result4 = collection.count_documents(query4)

    # все записи, количество которых больше 100.
    query5 = {"Count": {"$gt": 100}}
    result5 = list(collection.find(query5))

    os.makedirs("results", exist_ok=True)

    insert_data(os.path.join("results", "result1.json"), result1)
    insert_data(os.path.join("results", "result2.json"), result2)
    insert_data(os.path.join("results", "result3.json"), result3)
    insert_data(os.path.join("results", "result4.json"), result4)
    insert_data(os.path.join("results", "result5.json"), result5)

    # вывод минимального, среднего, максимального числа имен
    pipeline1 = [
        {
            "$group": {
                "_id": None,
                "min_count": {"$min": "$Count"},
                "avg_count": {"$avg": "$Count"},
                "max_count": {"$max": "$Count"},
            }
        }
    ]
    result1 = list(collection.aggregate(pipeline1))

    # вывод количества документов по национальности
    pipeline2 = [{"$group": {"_id": "$Ethnicity", "count": {"$count": {}}}}]
    result2 = list(collection.aggregate(pipeline2))

    # вывод минимального, среднего, максимального ранга по имени
    pipeline3 = [
        {
            "$group": {
                "_id": "$Child's First Name",
                "min_rank": {"$min": "$Rank"},
                "avg_rank": {"$avg": "$Rank"},
                "max_rank": {"$max": "$Rank"},
            }
        }
    ]
    result3 = list(collection.aggregate(pipeline3))

    # вывод минимального, среднего, максимального ранга по имени и году рождения
    pipeline4 = [
        {
            "$group": {
                "_id": {"year": "$Year of Birth", "name": "$Child's First Name"},
                "min_rank": {"$min": "$Rank"},
                "avg_rank": {"$avg": "$Rank"},
                "max_rank": {"$max": "$Rank"},
            }
        }
    ]
    result4 = list(collection.aggregate(pipeline4))

    # вывод минимального, среднего, максимального количества по нациоанльности
    pipeline5 = [
        {
            "$group": {
                "_id": "$Ethnicity",
                "min_count": {"$min": "$Count"},
                "avg_count": {"$avg": "$Count"},
                "max_count": {"$max": "$Count"},
            }
        }
    ]
    result5 = list(collection.aggregate(pipeline5))

    insert_data(os.path.join("results", "result6.json"), result1)
    insert_data(os.path.join("results", "result7.json"), result2)
    insert_data(os.path.join("results", "result8.json"), result3)
    insert_data(os.path.join("results", "result9.json"), result4)
    insert_data(os.path.join("results", "result10.json"), result5)

    # удалить из коллекции документы по предикату: Count < 25 000 || Count > 175000
    query1 = {"$or": [{"Count": {"$lt": 10}}, {"Count": {"$gt": 100}}]}
    collection.delete_many(query1)

    # увеличить Count всех документов на 1
    update2 = {"$inc": {"Count": 1}}
    collection.update_many({}, update2)

    # поднять ранг на 2 для произвольно выбранных национальностей
    n_to_update = ["BLACK NON HISPANIC", "HISPANIC", "WHITE NON HISPANIC"]
    query3 = {"Ethnicity": {"$in": n_to_update}}
    update3 = {"$inc": {"Rank": 2}}
    collection.update_many(query3, update3)

    # уменьшить ранг на 2 для произвольно выбранных имен
    n_to_update = ["Mae", "Anthony", "Chelsea"]
    query3 = {"Child's First Name": {"$in": n_to_update}}
    update3 = {"$inc": {"Rank": -2}}
    collection.update_many(query3, update3)

    # удалить из коллекции записи по произвольному предикату
    query5 = {"Year of Birth": {"$lt": 2020}}
    collection.delete_many(query5)
