# database_handler.py
from pymongo import MongoClient
import config

client = MongoClient(config.DB_HOST, int(config.DB_PORT))
print("Подключение к MongoDB установлено")  # Проверка подключения к MongoDB

db = client['e-commerce']
collection = db['products']

def get_shop_info(shop_name):
    """
    Возвращает подробную информацию о магазине по его имени.
    """
    data = collection.find_one()
    for shop in data['shops']:
        if shop['name'] == shop_name:
            return shop
    return None

def get_all_shops():
    """
    Возвращает краткую информацию обо всех магазинах.
    """
    data = collection.find_one()
    return data['shops'] if 'shops' in data else []




def get_products_in_shop(shop_name):
    """
    Возвращает список товаров, доступных в указанном магазине.
    """
    shop_info = get_shop_info(shop_name)
    if shop_info is not None:
        return shop_info['products']
    return None

def get_shops_by_brand(brand_name):
    """
    Возвращает все магазины определённого бренда.
    """
    brand_shops = collection.find({"brand": brand_name})
    return brand_shops
