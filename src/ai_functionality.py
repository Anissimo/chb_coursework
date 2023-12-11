# ai_functionality.py
from connections import get_collection
from connections import nlp
from fuzzysearch import find_near_matches
from transliterate import translit, get_available_language_codes

def find_best_match(input_string):
    doc = nlp(input_string)

    collection = get_collection()
    
    matches = []
    universal_break = False
    for item in collection.find():
        for value in item.items():
            for token in doc:
                # Попытка транслитерации токена
                try:
                    token_translit = translit(str(token), 'ru', reversed=True)
                except:
                    token_translit = str(token)

                found_matches = find_near_matches(token_translit, str(value), max_l_dist=1)
                if found_matches:
                    universal_break = True
                    matches.append((found_matches[0].dist, item))
                    break  # прерываем цикл после первого совпадения
            if universal_break: break
    
    # Сортировка совпадений по расстоянию Левенштейна
    matches.sort(key=lambda x: x[0])
    
    return matches
