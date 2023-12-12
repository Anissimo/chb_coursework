# keyboards.py
from telebot import types

def generate_markup(match):
    markup = types.InlineKeyboardMarkup()
    website_button = types.InlineKeyboardButton(text='Официальный сайт', url=match[1]['website'])
    markup.add(website_button)
    for show in match[1]['shows']:
        show_button = types.InlineKeyboardButton(text=show['title'], callback_data=f"show_info:{show['title']}")
        markup.add(show_button)
    more_info_button = types.InlineKeyboardButton(text='Больше информации', callback_data=f"more_info:{match[1]['_id']}")
    another_theater_button = types.InlineKeyboardButton(text='Хочу узнать о другом театре', callback_data="another_theater")
    markup.add(more_info_button, another_theater_button)
    return markup


def format_info(info):
    formatted_info = f"Театр: {info['theaterName']}\n"
    formatted_info += f"Официальный сайт: {info['website']}\n"
    formatted_info += f"Местоположение: {info['location']}\n"
    formatted_info += "Спектакли:\n"
    for show in info['shows']:
        formatted_info += f"Название: {show['title']}\n"
        formatted_info += f"Краткое описание: {show['shortDescription']}\n"
        formatted_info += "Предстоящие представления:\n"
        for upcoming_show in show['upcomingShows']:
            formatted_info += f"Дата: {upcoming_show['date']}\n"
            formatted_info += f"Стоимость билетов: {upcoming_show['ticketPrice']}\n"
            formatted_info += f"Ссылка для бронирования: {upcoming_show['bookingLink']}\n"
    return formatted_info


