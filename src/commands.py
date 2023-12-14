# commands.py
import database
from datetime import datetime
from geopy.geocoders import Nominatim
from telebot import types
import requests

def is_valid_url(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except:
        return False

def start(bot, message):
    "Отправляет приветственное сообщение и краткое описание функционала бота."
    bot.send_message(message.chat.id, 'Привет!')

def short(bot, message):
    "Отправляет краткую информацию о каждом театре."
    theaters = database.get_theaters()
    for theater in theaters:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Сайт", url=theater["website"]))
        location_url = theatre_location(bot, message, str(theater["_id"]), send_message=False)
        markup.add(types.InlineKeyboardButton(text="Адрес", url=location_url))
        bot.send_photo(chat_id=message.chat.id, photo=theater["theaterImages"][0], caption=f'ID: {str(theater["_id"])}\nНазвание театра: {theater["theaterName"]}\nСайт: {theater["website"]}\nМестоположение: {theater["location"]}\nКоличество спектаклей: {len(theater["shows"])}', reply_markup=markup)


def full(bot, message, theater_name):
    print("Вход в функцию full")
    theater = database.get_theater_by_name(theater_name)
    if theater is not None:
        print(f"Обработка театра {theater['theaterName']}")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Сайт", url=theater["website"]))
        location_url = theatre_location(bot, message, theater["_id"], send_message=False)
        markup.add(types.InlineKeyboardButton(text="Адрес", url=location_url))
        for show in theater["shows"]:
            markup.add(types.InlineKeyboardButton(text=show["title"], callback_data=f'show_info:{theater["_id"]}:{show["title"]}'))
        bot.send_photo(chat_id=message.chat.id, photo=theater["theaterImages"][0], caption=f'ID: {str(theater["_id"])}\n{theater["theaterName"]}\nАдрес: {theater["location"]}', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Театр с таким названием не найден.')


def show_info(bot, message, id=None, show_title=None, send_images=False):
    print("Вход в функцию show_info")
    theaters = database.get_theaters()
    for theater in theaters:
        for show in theater["shows"]:
            if show["title"] == show_title:
                print(f"Обработка шоу {show['title']}")
                markup = types.InlineKeyboardMarkup()
                upcoming_shows = [s for s in show["upcomingShows"] if datetime.fromisoformat(s["date"]) > datetime.now()]
                if upcoming_shows:
                    # Проверяем, является ли дата строкой
                    if isinstance(upcoming_shows[0]["date"], str):
                        show_date = upcoming_shows[0]["date"]
                    else:
                        show_date = upcoming_shows[0]["date"].strftime("%d.%m.%Y %H:%M")
                    markup.add(types.InlineKeyboardButton(text="Бронировать билеты", url=upcoming_shows[0]["bookingLink"]))
                    for image in show["images"]:
                        if is_valid_url(image):
                            bot.send_photo(chat_id=message.chat.id, photo=image, caption=f'Название спектакля: {show["title"]}\nБлижайший спектакль: {show_date}\nЦена билета: {upcoming_shows[0]["ticketPrice"]}', reply_markup=markup)
                            break
                return
    bot.send_message(message.chat.id, 'Спектакль с таким названием не найден.')


def nearest_show(bot, message, theater_name=None, show_title=None):
    print("Вход в функцию nearest_show")
    if theater_name is not None:
        theaters = [database.get_theater_by_name(theater_name)]
    elif show_title is not None:
        theaters = database.get_theaters()
    else:
        theaters = database.get_theaters()  # Возвращаем спектакли всех театров, если не указаны theater_name и show_title
    for theater in theaters:
        if theater is not None:
            print(f"Обработка театра {theater['theaterName']}")
            for show in theater["shows"]:
                if show_title is not None and show["title"] != show_title:
                    continue
                upcoming_shows = [s for s in show["upcomingShows"] if datetime.fromisoformat(s["date"]) > datetime.now()]
                if upcoming_shows:
                    # Обновляем дату ближайшего спектакля в информации о спектакле
                    show["upcomingShows"][0]["date"] = upcoming_shows[0]["date"]
                    show_info(bot, message, str(theater["_id"]), show["title"], send_images=False)
        else:
            bot.send_message(message.chat.id, 'Театр с таким названием не найден.')



def theatre_location(bot, message, id, send_message=True):
    print("Вход в функцию theatre_location")
    theater = database.get_theater(id)
    if theater is not None:
        print(f"Обработка театра {theater['theaterName']}")
        geolocator = Nominatim(user_agent="theatre_bot")
        location = geolocator.geocode(theater["location"])
        yandex_maps_link = f'https://yandex.com/maps/?ll={location.longitude},{location.latitude}&z=14'
        if send_message:
            bot.send_message(message.chat.id, f'Как добраться? \n{theater["theaterName"]}\nЯндекс Карты\n{yandex_maps_link}')
        return yandex_maps_link
    else:
        if send_message:
            bot.send_message(message.chat.id, 'Театр с таким ID не найден.')
        return None

def feedback(bot, message):
    "Позволяет пользователю оставить отзыв или предложение."
    id = message.text[11:-1]  # Извлекаем id из команды
    theater = database.get_theater(id)
    if theater is not None:
        bot.send_message(message.chat.id, 'Пожалуйста, напишите свой отзыв.')
        bot.register_next_step
