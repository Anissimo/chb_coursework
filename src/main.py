# main.py
import telebot
from telebot import types

import config, command_handler, database_handler, nlp_handler, user_interface

bot = telebot.TeleBot(config.BOT_TOKEN)
user_interface.set_bot(bot)  # Добавьте эту строку

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Привет')
    itembtn2 = types.KeyboardButton('Помощь')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Привет! Я бот магазина компьютерных комплектующих. Чем я могу помочь?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Привет')
def greet(message):
    bot.reply_to(message, "Привет! Чем я могу помочь?")

@bot.message_handler(func=lambda message: message.text == 'Помощь')
def help(message):
    command_handler.handle_help_button(bot, message)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'shop_info':
        user_interface.ask_for_shop(call.message)
    elif call.data == 'all_shops':
        user_interface.send_all_shops(bot, call.message)
    elif call.data == 'shop_products':
        user_interface.ask_for_shop(call.message)
    elif call.data == 'brand_shops':
        user_interface.ask_for_shop(call.message)

bot.polling()
