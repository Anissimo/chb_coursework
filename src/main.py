"""
Главный файл бота. Этот файл служит точкой входа для бота.
Он импортирует и использует модули из каталога 'modules'.
"""

import telebot
from modules import config, command_handler, database_handler, nlp_handler, user_interface

bot = telebot.TeleBot(config.BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот магазина компьютерных комплектующих. Чем я могу помочь?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()
