from connections import bot
from connections import get_more_info
from keyboards import generate_markup, format_info
from ai_functionality import find_best_match

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! О каком бренде ты хотел бы узнать?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text
    matches = find_best_match(text)
    if matches:
        for match in matches:
            try:
                markup = generate_markup(match)
                bot.send_message(message.chat.id, f"{match[1]['history']}\n", reply_markup=markup)
            except Exception as e:
                print(f"Error sending message: {e}")
                bot.send_message(message.chat.id, "Упс, попробуй ввести данные заного =)")
    else:
        bot.reply_to(message, "Кажется такого у меня нет =(")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data.split(":")
    if data[0] == "more_info":
        more_info = get_more_info(data[1])
        formatted_info = format_info(more_info)
        bot.send_message(call.message.chat.id, formatted_info)
    elif data[0] == "another_brand":
        bot.send_message(call.message.chat.id, "Пожалуйста, введите название другого бренда, который вы хотите исследовать.")


bot.polling()
