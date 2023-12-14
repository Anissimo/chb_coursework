# main.py
import telebot
import config
import commands
from telebot import types
from searcher import Searcher

# searcher = Searcher()
searcher = None
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

@bot.callback_query_handler(func=lambda call: call.data == 'show_info')
def callback_show_info(call):
    bot.send_message(call.message.chat.id, 'Пожалуйста, введите название спектакля.')
    bot.register_next_step_handler(call.message, process_show_title)

@bot.callback_query_handler(func=lambda call: call.data.startswith('show_info:'))
def callback_show_info_specific(call):
    _, id, show_title = call.data.split(':')
    commands.show_info(bot, call.message, id=id, show_title=show_title)


@bot.callback_query_handler(func=lambda call: call.data == 'nearest_show_all')
def callback_nearest_show_all(call):
    commands.nearest_show(bot, call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'nearest_show_id')
def callback_nearest_show_id(call):
    bot.send_message(call.message.chat.id, 'Пожалуйста, введи название театра.')
    bot.register_next_step_handler(call.message, process_theatre_name_nearest_show)

@bot.callback_query_handler(func=lambda call: call.data == 'nearest_show_title')
def callback_nearest_show_title(call):
    bot.send_message(call.message.chat.id, 'Пожалуйста, введи название спектакля.')
    bot.register_next_step_handler(call.message, process_show_title_nearest_show)

def process_theatre_name_nearest_show(message):
    commands.nearest_show(bot, message, theater_name=message.text)

def process_show_title_nearest_show(message):
    commands.nearest_show(bot, message, show_title=message.text)



def process_theatre_name_full(message):
    commands.full(bot, message, theater_name=message.text)

def process_show_title_show_info(message):
    commands.show_info(bot, message, show_title=message.text)





def process_show_title(message):
    print(f"Название спектакля: {message.text}")
    commands.show_info(bot, message, show_title=message.text)


def process_theatre_id(message):
    commands.full(bot, message, message.text)




@bot.callback_query_handler(func=lambda call: call.data == 'search')
def callback_search(call):
    global searcher
    searcher = Searcher()
    bot.send_message(call.message.chat.id, 'Введите ваше сообщение.')
    bot.register_next_step_handler(call.message, process_search_query)

def process_search_query(message):
    global searcher
    action = searcher.predict_action(message.text)
    searcher = None
    if action == 'start':
        commands.start(bot, message)
    elif action == 'help':
        help(message)
    elif action == 'short':
        commands.short(bot, message)
    elif action == 'full':
        bot.send_message(message.chat.id, 'Пожалуйста, введите название театра.')
        bot.register_next_step_handler(message, process_theatre_name_full)
    elif action == 'show_info':
        bot.send_message(message.chat.id, 'Пожалуйста, введите название спектакля.')
        bot.register_next_step_handler(message, process_show_title_show_info)
    elif action == 'nearest_show_all':
        commands.nearest_show(bot, message)
    elif action == 'nearest_show_id':
        bot.send_message(message.chat.id, 'Пожалуйста, введите название театра.')
        bot.register_next_step_handler(message, process_theatre_name_nearest_show)
    elif action == 'nearest_show_title':
        bot.send_message(message.chat.id, 'Пожалуйста, введите название спектакля.')
        bot.register_next_step_handler(message, process_show_title_nearest_show)


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f'Ошибка: {e}')
