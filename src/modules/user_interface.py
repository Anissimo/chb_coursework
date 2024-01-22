"""
Модуль взаимодействия с пользователем. Этот модуль содержит функции для формирования ответов бота и отправки их пользователям.
"""

# user_interface.py
from telebot import types
import database_handler

def send_shop_info(bot, message, shop_name):
    """
    Отправляет подробную информацию о магазине пользователю.
    """
    shop_info = database_handler.get_shop_info(shop_name)
    if shop_info is not None:
        bot.reply_to(message, str(shop_info))
    else:
        bot.reply_to(message, "Извините, я не могу найти информацию об этом магазине.")

def send_all_shops(bot, message):
    """
    Отправляет краткую информацию обо всех магазинах пользователю.
    """
    all_shops = database_handler.get_all_shops()
    for shop in all_shops:
        bot.send_message(message.chat.id, str(shop))

def send_products_in_shop(bot, message, shop_name):
    """
    Отправляет список товаров, доступных в указанном магазине, пользователю.
    """
    products_in_shop = database_handler.get_products_in_shop(shop_name)
    if products_in_shop is not None:
        for product in products_in_shop:
            bot.send_message(message.chat.id, str(product))
    else:
        bot.reply_to(message, "Извините, я не могу найти информацию о товарах в этом магазине.")

def send_shops_by_brand(bot, message, brand_name):
    """
    Отправляет все магазины определённого бренда пользователю.
    """
    brand_shops = database_handler.get_shops_by_brand(brand_name)
    if brand_shops is not None:
        for shop in brand_shops:
            bot.send_message(message.chat.id, str(shop))
    else:
        bot.reply_to(message, "Извините, я не могу найти магазины этого бренда.")
