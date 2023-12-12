# commands.py

import database
from datetime import datetime
from geopy.geocoders import Nominatim

def start(bot, message):
    "Отправляет приветственное сообщение и краткое описание функционала бота."
    bot.send_message(message.chat.id, 'Привет!')

def help(bot, message):
    "Показывает список всех доступных команд."
    bot.send_message(message.chat.id, 'Вот список всех доступных команд:\n\n/start - Приветственное сообщение и краткое описание функционала бота.\n/help - Показывает список всех доступных команд.\n/short - Показывает краткую информацию о каждом театре.\n/id(театра)/full - Показывает полную информацию о театре с указанным ID.\n/id(театра)/full/show_title - Показывает информацию о конкретном спектакле в указанном театре.\n/nearest_show/all - Показывает ближайшие спектакли всех театров.\n/id(театра)/nearest_show - Показывает ближайшие спектакли конкретного театра.\n/show_title/nearest_show - Показывает ближайшие спектакли с указанным названием.\n/id(театра)/location - Показывает местоположение театра с указанным ID на Яндекс Картах.\n/search - Выполняет умный поиск на основе запроса пользователя и вызывает наиболее подходящую функцию.')


def short(bot, message):
    "Отправляет краткую информацию о каждом театре."
    theaters = database.get_theaters()
    for theater in theaters:
        bot.send_message(message.chat.id, f'ID: {str(theater["_id"])}\nНазвание театра: {theater["theaterName"]}\nСайт: {theater["website"]}\nМестоположение: {theater["location"]}\nКоличество спектаклей: {len(theater["shows"])}')

def full(bot, message, id):
    # /full/65780c052c563c97e5e7b1a1
    print("Вход в функцию full")
    theater = database.get_theater(id)
    if theater is not None:
        print(f"Обработка театра {theater['theaterName']}")
        bot.send_message(message.chat.id, f'ID: {str(theater["_id"])}\nНазвание театра: {theater["theaterName"]}\nСайт: {theater["website"]}\nМестоположение: {theater["location"]}')
        for image_url in theater["theaterImages"]:
            bot.send_photo(chat_id=message.chat.id, photo=image_url)
        for show in theater["shows"]:
            show_info(bot, message, id, show["title"], send_images=True)
    else:
        bot.send_message(message.chat.id, 'Театр с таким ID не найден.')

def show_info(bot, message, id, show_title, send_images=False):
    # /full/65780c052c563c97e5e7b1a1/Ревизор
    print("Вход в функцию show_info")
    theater = database.get_theater(id)
    if theater is not None:
        for show in theater["shows"]:
            if show["title"] == show_title:
                print(f"Обработка шоу {show['title']}")
                bot.send_message(message.chat.id, f'Название спектакля: {show["title"]}\nКраткое описание: {show["shortDescription"]}')
                if send_images:
                    for image_url in show["images"]:
                        bot.send_photo(chat_id=message.chat.id, photo=image_url)
                for upcoming_show in show["upcomingShows"]:
                    bot.send_message(message.chat.id, f'Дата: {upcoming_show["date"]}\nЦена билета: {upcoming_show["ticketPrice"]}\nСсылка на бронирование: {upcoming_show["bookingLink"]}')
    else:
        bot.send_message(message.chat.id, 'Театр с таким ID не найден.')

def nearest_show(bot, message, id=None, title=None):
    print("Вход в функцию nearest_show")
    if id is not None:
        theaters = [database.get_theater(id)]
    elif title is not None:
        theaters = database.get_theaters()
    else:
        return
    for theater in theaters:
        if theater is not None:
            print(f"Обработка театра {theater['theaterName']}")
            for show in theater["shows"]:
                if title is not None and show["title"] != title:
                    continue
                upcoming_shows = [s for s in show["upcomingShows"] if datetime.fromisoformat(s["date"]) > datetime.now()]
                if upcoming_shows:
                    bot.send_message(message.chat.id, f'Название спектакля: {show["title"]}\nБлижайший спектакль: {upcoming_shows[0]["date"]}\nЦена билета: {upcoming_shows[0]["ticketPrice"]}\nСсылка на бронирование: {upcoming_shows[0]["bookingLink"]}')
        else:
            bot.send_message(message.chat.id, 'Театр с таким ID не найден.')

from geopy.geocoders import Nominatim

def theatre_location(bot, message, id):
    print("Вход в функцию theatre_location")
    theater = database.get_theater(id)
    if theater is not None:
        print(f"Обработка театра {theater['theaterName']}")
        geolocator = Nominatim(user_agent="theatre_bot")
        location = geolocator.geocode(theater["location"])
        yandex_maps_link = f'https://yandex.com/maps/?ll={location.longitude},{location.latitude}&z=14'
        bot.send_message(message.chat.id, f'Местоположение театра {theater["theaterName"]}\nЯндекс Карты\n{yandex_maps_link}')
    else:
        bot.send_message(message.chat.id, 'Театр с таким ID не найден.')


def feedback(bot, message):
    "Позволяет пользователю оставить отзыв или предложение."
    id = message.text[11:-1]  # Извлекаем id из команды
    theater = database.get_theater(id)
    if theater is not None:
        bot.send_message(message.chat.id, 'Пожалуйста, напишите свой отзыв.')
        bot.register_next_step