# main.py
import telebot
import config
import commands
import searcher
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


@bot.message_handler(commands=['short'])
def short(message):
    commands.short(bot, message)


@bot.message_handler(regexp=r'^/full/\w+$')
def full(message):
    print("Обработка команды /full")
    id = message.text.split('/')[2]  # Извлекаем id из команды
    commands.full(bot, message, id)


@bot.message_handler(regexp=r'^/full/\w+/\w+$')
def show_info(message):
    print("Обработка команды /full/show")
    id, show_title = message.text.split('/')[2:]  # Извлекаем id и название шоу из команды
    commands.show_info(bot, message, id, show_title, send_images=False)

# @bot.callback_query_handler(func=lambda call: call.data.startswith('show_info'))
# def callback_query(call):
#     _, id, show_title = call.data.split(':')
#     commands.show_info(bot, call.message, id, show_title, send_images=True)


@bot.message_handler(regexp=r'^/nearest_show/all$')
def nearest_show_all(message):
    print("Обработка команды /nearest_show/all")
    commands.nearest_show(bot, message)

@bot.message_handler(regexp=r'^/nearest_show/\w+$')
def nearest_show_id(message):
    print("Обработка команды /nearest_show/id")
    id = message.text.split('/')[2]  # Извлекаем id из команды
    commands.nearest_show(bot, message, id)

@bot.message_handler(regexp=r'^/nearest_show/\w+$')
def nearest_show_title(message):
    print("Обработка команды /nearest_show/title")
    title = message.text.split('/')[2]  # Извлекаем название из команды
    commands.nearest_show(bot, message, title=title)

@bot.message_handler(regexp=r'^/\w+/location$')
def theatre_location(message):
    print("Обработка команды /id/location")
    id = message.text.split('/')[1]  # Извлекаем id из команды
    commands.theatre_location(bot, message, id)

# @bot.message_handler(regexp=r'^/feedback$')
# def feedback(message):
#     commands.feedback(bot, message)

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
    print("Вход в функцию callback_show_info")
    bot.send_message(call.message.chat.id, 'Пожалуйста, введите название спектакля.')
    bot.register_next_step_handler(call.message, process_show_title)

def process_show_title(message):
    print("Вход в функцию process_show_title")
    print(f"Название спектакля: {message.text}")
    commands.show_info(bot, message, show_title=message.text)





@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    # Проверяем, содержит ли сообщение '/'
    if '/' not in message.text:
        print("Обработка всех сообщений")
        searcher.search(bot, message)



if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f'Ошибка: {e}')
