# command_handler.py
from telebot import types
# from modules import database_handler

def handle_help_button(bot, message):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Информация о конкретном магазине', callback_data='shop_info')
    itembtn2 = types.InlineKeyboardButton('Информация о всех магазинах', callback_data='all_shops')
    itembtn3 = types.InlineKeyboardButton('Товары в конкретном магазине', callback_data='shop_products')
    itembtn4 = types.InlineKeyboardButton('Все магазины определённого бренда', callback_data='brand_shops')
    itembtn5 = types.InlineKeyboardButton('Поиск', callback_data='search')

    markup.add(itembtn1)
    markup.add(itembtn2)
    markup.add(itembtn3)
    markup.add(itembtn4)
    markup.add(itembtn5)
    bot.send_message(message.chat.id, "Выберите одну из следующих опций:", reply_markup=markup)
