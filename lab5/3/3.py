import pickle
import sys

sys.path.append("..")
from database_utils import connect_to_mongo

with open("task_3_item.pkl", "rb") as f:
    data = pickle.load(f)

with connect_to_mongo("test", "jobs") as collection:
    collection.insert_many(data)

    # удалить из коллекции документы по предикату: salary < 25 000 || salary > 175000
    query1 = {"$or": [{"salary": {"$lt": 25000}}, {"salary": {"$gt": 175000}}]}
    collection.delete_many(query1)

    # увеличить возраст (age) всех документов на 1
    update2 = {"$inc": {"age": 1}}
    collection.update_many({}, update2)

    # поднять заработную плату на 5% для произвольно выбранных профессий
    professions_to_update = ["Программист", "Инженер", "Косметолог"]
    query3 = {"job": {"$in": professions_to_update}}
    update3 = {"$mul": {"salary": 1.05}}
    collection.update_many(query3, update3)

    # поднять заработную плату на 7% для произвольно выбранных городов
    cities_to_update = ["city1", "city2", "city3"]
    query4 = {"city": {"$in": cities_to_update}}
    update4 = {"$mul": {"salary": 1.07}}
    collection.update_many(query4, update4)

    # поднять заработную плату на 10% для выборки по сложному предикату (произвольный город, произвольный набор профессий, произвольный диапазон возраста)
    query5 = {
        "city": "Бургос",
        "job": {"$in": ["Программист", "Инженер", "Косметолог"]},
        "age": {"$gte": 25, "$lte": 35},
    }
    update5 = {"$mul": {"salary": 1.1}}
    collection.update_many(query5, update4)

    # удалить из коллекции записи по произвольному предикату
    query6 = {"year": {"$lt": 2010}}
    collection.delete_many(query6)
