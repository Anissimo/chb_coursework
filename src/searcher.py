from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import commands
import database

# Словарь с типовыми фразами пользователей
user_phrases = {
    'short': ['расскажи о театрах', 'информация о театрах', 'список театров', 'дай информацию о театрах', 'покажи театры', 'хочу узнать о театрах'],
    'full': ['хочу узнать о театре', 'полная информация о театре', 'всё о театре', 'расскажи мне о театре', 'дай информацию о театре', 'подробности о театре'],
    'nearest_show': ['ближайшие спектакли', 'предстоящие спектакли', 'скорые премьеры', 'когда следующий спектакль', 'ближайшие даты спектаклей', 'расписание спектаклей'],
    'location': ['где находится театр', 'местоположение театра', 'адрес театра', 'покажи театр на карте', 'как добраться до театра', 'где расположен театр']
}

# Создаём векторизатор TF-IDF
vectorizer = TfidfVectorizer()
vectorized_phrases = vectorizer.fit_transform([' '.join(phrases) for phrases in user_phrases.values()])

def search(bot, message):
    try:
        # Векторизуем запрос пользователя
        user_query = vectorizer.transform([message.text])
        
        # Вычисляем косинусное сходство между запросом пользователя и типовыми фразами
        similarities = cosine_similarity(user_query, vectorized_phrases).flatten()
        
        # Находим индекс фразы с наибольшим сходством
        best_match_index = similarities.argmax()
        
        # Вызываем соответствующую функцию
        if best_match_index == 0:
            commands.short(bot, message)
        elif best_match_index == 1:
            # Ищем в базе данных театр, который упоминается в запросе пользователя
            theater_name = database.find_theater_in_text(message.text)
            if theater_name:
                commands.full(bot, message, theater_name)
            else:
                bot.send_message(message.chat.id, "Попробуйте найти ещё")
        elif best_match_index == 2:
            commands.nearest_show(bot, message)
        elif best_match_index == 3:
            commands.theatre_location(bot, message)
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(message.chat.id, "Попробуйте найти ещё")
