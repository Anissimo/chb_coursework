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
    print("Обработка сообщения пользователя")
    # Векторизуем запрос пользователя
    user_query = vectorizer.transform([message.text])
    
    # Вычисляем косинусное сходство между запросом пользователя и типовыми фразами
    similarities = cosine_similarity(user_query, vectorized_phrases).flatten()
    print(f"Косинусное сходство: {similarities}")
    
    # Находим индекс фразы с наибольшим сходством
    best_match_index = similarities.argmax()
    print(f"Лучший индекс совпадения: {best_match_index}")
    
    # Вызываем соответствующую функцию
    if best_match_index == 0:
        print("Вызов функции commands.short")
        commands.short(bot, message)
    elif best_match_index == 1:
        print("Вызов функции commands.full")
        commands.full(bot, message)
    elif best_match_index == 2:
        print("Вызов функции commands.nearest_show")
        commands.nearest_show(bot, message)
    elif best_match_index == 3:
        print("Вызов функции commands.theatre_location")
        commands.theatre_location(bot, message)
