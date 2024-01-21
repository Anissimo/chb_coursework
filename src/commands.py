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
    print("Получение театров завершено")
    for theater in theaters:
        print(f"Обработка театра {theater['theaterName']}")
        for show in theater["shows"]:
            print(f"Обработка шоу {show['title']}")
            if show["title"] == show_title:
                print(f"Найдено шоу {show['title']}")
                markup = types.InlineKeyboardMarkup()
                upcoming_shows = [s for s in show["upcomingShows"] if datetime.fromisoformat(s["date"]) > datetime.now()]
                print(f"Найдено {len(upcoming_shows)} предстоящих шоу")
                if upcoming_shows:
                    print("Обработка предстоящих шоу")
                    if isinstance(upcoming_shows[0]["date"], str):
                        show_date = upcoming_shows[0]["date"]
                    else:
                        show_date = upcoming_shows[0]["date"].strftime("%d.%m.%Y %H:%M")
                    markup.add(types.InlineKeyboardButton(text="Бронировать билеты", url=upcoming_shows[0]["bookingLink"]))
                    for image in show["images"]:
                        print(f"Обработка изображения {image}")
                        if is_valid_url(image):
                            print("Отправка фото")
                            bot.send_photo(chat_id=message.chat.id, photo=image, caption=f'Название спектакля: {show["title"]}\nБлижайший спектакль: {show_date}\nЦена билета: {upcoming_shows[0]["ticketPrice"]}', reply_markup=markup)
                            print("Фото отправлено")
                            break
                print("Выход из цикла обработки шоу")
                return
    print("Отправка сообщения об ошибке")
    bot.send_message(message.chat.id, 'Спектакль с таким названием не найден.')
    print('Выход из метода show_info')


def nearest_show(bot, message, theater_name=None, show_title=None):
    print("qВход в функцию nearest_show")
    if theater_name is not None:
        print("qПолучение театра по имени")
        theaters = [database.get_theater_by_name(theater_name)]
    elif show_title is not None:
        print("qПолучение всех театров")
        theaters = database.get_theaters()
    else:
        print("qПолучение всех театров")
        theaters = database.get_theaters()  # Возвращаем спектакли всех театров, если не указаны theater_name и show_title
    for theater in theaters:
        if theater is not None:
            print(f"Обработка театра {theater['theaterName']}")
            for show in theater["shows"]:
                print(f"qОбработка шоу {show['title']}")
                if show_title is not None and show["title"] != show_title:
                    print("qПропуск шоу, так как оно не соответствует заданному названию")
                    continue
                upcoming_shows = [s for s in show["upcomingShows"] if datetime.fromisoformat(s["date"]) > datetime.now()]
                print(f"qНайдено {len(upcoming_shows)} предстоящих шоу")
                if upcoming_shows:
                    print("qОбработка предстоящих шоу")
                    show["upcomingShows"][0]["date"] = upcoming_shows[0]["date"]
                    print("qВызов функции show_info")
            # bot.send_message(message.chat.id, 'Театр с таким названием не найден.')
    print('qВыход из метода nearest_show')




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
