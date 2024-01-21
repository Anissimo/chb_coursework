# database.py

from pymongo import MongoClient
from bson.objectid import ObjectId
import config

client = MongoClient(config.MONGODB_SERVER)
db = client['theatre']
theaters = db['firstCollection']


def get_theaters():
    "Возвращает все театры"
    result = theaters.find()
    return result

def get_theater_by_name(theater_name):
    print("Получение театра с указанным названием из базы данных")
    result = theaters.find_one({"theaterName": theater_name})
    if result is not None:
        print(f"Театр {result['theaterName']} найден"   )
    else:
        print("Театр не найден")
    return result


def get_theater(id):
    print("Получение театра с указанным ID из базы данных")
    result = theaters.find_one({"_id": ObjectId(id)})
    if result is not None:
        print(f"Театр {result['theaterName']} найден")
    else:
        print("Театр не найден")
    return result




def add_feedback(theater, feedback):
    "Добавляет отзыв к указанному театру"
    theaters.update_one({"_id": theater["_id"]}, {"$push": {"feedback": feedback}})
