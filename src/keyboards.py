# keyboards.py
from telebot import types

def generate_markup(match):
    markup = types.InlineKeyboardMarkup()
    website_button = types.InlineKeyboardButton(text='Официальный сайт', url=match[1]['official_website'])
    markup.add(website_button)
    for store in match[1]['stores']:
        store_button = types.InlineKeyboardButton(text=store['name'], url=store['url'])
        markup.add(store_button)
    more_info_button = types.InlineKeyboardButton(text='Больше информации', callback_data=f"more_info:{match[1]['_id']}")
    another_brand_button = types.InlineKeyboardButton(text='Хочу узнать о другом бренде', callback_data="another_brand")
    markup.add(more_info_button, another_brand_button)
    return markup

def format_info(info):
    formatted_info = f"Бренд: {info['brand']}\n"
    formatted_info += f"Официальный сайт: {info['official_website']}\n"
    formatted_info += "Магазины:\n"
    for store in info['stores']:
        formatted_info += f"Название: {store['name']}\n"
        formatted_info += f"Сайт: {store['url']}\n"
        formatted_info += f"Информация о заказе: {store['order_info']}\n"
        formatted_info += f"Местоположение: {store['location']}\n"
    return formatted_info

