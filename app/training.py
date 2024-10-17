import re
from transformers import pipeline

# Загружаем многоязычную модель для классификации текста
nlp_model = pipeline("text-classification", model="distilbert-base-uncased")

# Словарь популярных моделей смартфонов
known_models = [
    "iphone 15", "iphone 15 pro", "iphone 15 pro max",
    "iphone 14", "iphone 14 pro", "iphone 13",
    "iphone 13 mini", "iphone 12", "iphone se (2022)",
    "iphone xr", "samsung galaxy s23",
    "samsung galaxy s23 ultra", "samsung galaxy s22",
    "samsung galaxy s21", "samsung galaxy a54",
    "samsung galaxy a34", "samsung galaxy z fold 5",
    "samsung galaxy z flip 5", "samsung galaxy m54",
    "samsung galaxy f14"
]

# Определение намерения пользователя
def classify_intent(user_input):
    # Проверяем наличие ключевых слов для понимания намерения
    keywords_compare = ["разница", "сравнить", "сравнение", "различие"]
    keywords_price = ["сколько стоит", "цена", "стоимость", "сколько"]

    if any(keyword in user_input for keyword in keywords_compare):
        return "COMPARE"
    elif any(keyword in user_input for keyword in keywords_price):
        return "PRICE"
    else:
        # Классификация намерений с использованием многоязычной модели
        intent = nlp_model(user_input)[0]['label']
        print(intent)
        return intent

# Функция для извлечения моделей из пользовательского запроса
def extract_models_from_query(user_input, flag):
    user_input = user_input.lower()
    found_models = []

    sorted_models = sorted(known_models, key=len, reverse=True)

    if flag == 'PRICE':
        for model in sorted_models:
            if re.search(re.escape(model), user_input):
                found_models.append(model)
                # Прерываем поиск, если находим наиболее специфическую модель
                break
    elif flag == 'COMPARE':
        for model in sorted_models:
            if re.search(re.escape(model), user_input):
                found_models.append(model)

    print(found_models)

    return found_models  # Возвращаем найденные модели без ограничения



# Основная логика обработки запросов
def handle_request(user_input):
    # Определение намерения пользователя
    intent = classify_intent(user_input)

    # Извлечение моделей из запроса
    models = extract_models_from_query(user_input, intent)

    return intent, models