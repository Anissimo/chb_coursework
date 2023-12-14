# main.py
import telebot
import config
import commands
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    commands.start(bot, message)

@bot.message_handler(commands=['help'])
def help(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Приветственное сообщение", callback_data='start'))
    markup.add(types.InlineKeyboardButton(text="Краткая информация о каждом театре", callback_data='short'))
    markup.add(types.InlineKeyboardButton(text="Полная информация о театре", callback_data='full'))
    markup.add(types.InlineKeyboardButton(text="Информация о конкретном спектакле", callback_data='show_info'))
    markup.add(types.InlineKeyboardButton(text="Ближайшие спектакли всех театров", callback_data='nearest_show_all'))
    markup.add(types.InlineKeyboardButton(text="Ближайшие спектакли конкретного театра", callback_data='nearest_show_id'))
    markup.add(types.InlineKeyboardButton(text="Ближайшие спектакли с указанным названием", callback_data='nearest_show_title'))
    markup.add(types.InlineKeyboardButton(text="Поиск", callback_data='search'))
    bot.send_message(message.chat.id, "Вот список всех доступных команд:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'start')
def callback_start(call):
    commands.start(bot, call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'short')
def callback_short(call):
    commands.short(bot, call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'full')
def callback_full(call):
    bot.send_message(call.message.chat.id, 'Пожалуйста, введи театр о котором ты хотел бы узнать')
    bot.register_next_step_handler(call.message, process_theatre_id)

def process_theatre_id(message):
    commands.full(bot, message, message.text)

@bot.callback_query_handler(func=lambda call: call.data == 'show_info')
def callback_show_info(call):
    bot.send_message(call.message.chat.id, 'Пожалуйста, введите название спектакля.')
    bot.register_next_step_handler(call.message, process_show_title)

def process_show_title(message):
    print(f"Название спектакля: {message.text}")
    commands.show_info(bot, message, show_title=message.text)

if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f'Ошибка: {e}')
