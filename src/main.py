"""
Главный файл бота. Этот файл служит точкой входа для бота.
Он импортирует и использует модули из каталога 'modules'.
"""

import telebot
from telebot import types

from .modules import config, command_handler, database_handler, nlp_handler, user_interface

# main.py
import telebot

bot = telebot.TeleBot(config.BOT_TOKEN)

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

bot.polling()
