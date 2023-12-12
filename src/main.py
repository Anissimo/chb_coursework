# main.py
import telebot
import config
import commands
import searcher

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    commands.start(bot, message)

@bot.message_handler(commands=['help'])
def help(message):
    commands.help(bot, message)

@bot.message_handler(commands=['short'])
def short(message):
    commands.short(bot, message)


@bot.message_handler(regexp=r'^/full/\w+$')
def full(message):
    print("Обработка команды /full")
    id = message.text.split('/')[2]  # Извлекаем id из команды
    commands.full(bot, message, id)

@bot.message_handler(regexp=r'^/upcoming_shows$')
def upcoming_shows(message):
    commands.upcoming_shows(bot, message)

@bot.message_handler(regexp=r'^/full/\w+/\w+$')
def show_info(message):
    print("Обработка команды /full/show")
    id, show_title = message.text.split('/')[2:]  # Извлекаем id и название шоу из команды
    commands.show_info(bot, message, id, show_title, send_images=False)


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    print("Обработка всех сообщений")
    searcher.search(bot, message)


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

@bot.message_handler(regexp=r'^/feedback$')
def feedback(message):
    commands.feedback(bot, message)

if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f'Ошибка: {e}')
