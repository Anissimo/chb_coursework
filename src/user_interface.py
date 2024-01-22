# user_interface.py
from telebot import types
import database_handler

bot = None

def set_bot(b):
    global bot
    bot = b

def ask_for_shop(message):
    msg = bot.send_message(message.chat.id, "Пожалуйста, введите название магазина.")
    bot.register_next_step_handler(msg, process_shop_step)

def process_shop_step(message):
    shop_name = message.text
    send_products_in_shop(message, shop_name)

def send_shop_info(message, shop_name):
    shop_info = database_handler.get_shop_info(shop_name)
    if shop_info is not None:
        info = f"**{shop_info['name']}**\n"
        info += f"Веб-сайт: {shop_info['website']}\n"
        info += f"Описание: {shop_info['description']}\n"
        info += "Местоположения:\n"
        for location in shop_info['locations']:
            info += f"  - Город: {location['city']}\n"
            info += f"    Адрес: {location['address']}\n"
            info += f"    Часы работы: {location['working_hours']}\n"
        bot.reply_to(message, info, parse_mode='Markdown')
    else:
        bot.reply_to(message, "Извините, я не могу найти информацию об этом магазине.")

def send_all_shops(bot, message):
    all_shops = database_handler.get_all_shops()
    info = "Вот список всех магазинов:\n"
    for shop in all_shops:
        info += f"- {shop['name']}\n"
    bot.send_message(message.chat.id, info, parse_mode='Markdown')

def send_products_in_shop(message, shop_name):
    products_in_shop = database_handler.get_products_in_shop(shop_name)
    if products_in_shop is not None:
        info = f"Вот товары, доступные в магазине {shop_name}:\n"
        for product in products_in_shop:
            info += f"- {product['name']}\n"
        bot.send_message(message.chat.id, info, parse_mode='Markdown')
    else:
        bot.reply_to(message, "Извините, я не могу найти информацию о товарах в этом магазине.")


def send_shops_by_brand(bot, message, brand_name):
    brand_shops = database_handler.get_shops_by_brand(brand_name)
    if brand_shops is not None:
        info = f"Вот магазины бренда {brand_name}:\n"
        for shop in brand_shops:
            info += f"- {shop['name']}\n"
        bot.send_message(message.chat.id, info, parse_mode='Markdown')
    else:
        bot.reply_to(message, "Извините, я не могу найти магазины этого бренда.")
