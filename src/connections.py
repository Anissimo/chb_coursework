# connections.py
import telebot
import spacy
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from bson.objectid import ObjectId

from config import TOKEN
from config import MONGODB_SERVER

nlp = spacy.load('en_core_web_sm')
bot = telebot.TeleBot(TOKEN)

# parsing from db
def get_collection():
    try:
        client = MongoClient(MONGODB_SERVER)
        client.server_info()  # Попытка подключения к серверу
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print("Не удалось подключиться к серверу MongoDB:", e)
        return None

    try:
        db = client['MusicBrands']
        collection = db['theatre']
        # print(collection)
        return collection
    except Exception as e:
        return None

def get_shows_info(item_id):
    collection = get_collection()
    item = collection.find_one({"_id": item_id})
    if item and 'shows' in item:
        return item['shows']
    else:
        return None
    

def get_more_info(item_id):
    collection = get_collection()
    item = collection.find_one({"_id": ObjectId(item_id)})
    if item:
        # Вернуть всю информацию о театре
        return item
    else:
        return None
    