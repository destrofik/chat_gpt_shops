import re
from fuzzywuzzy import process  # Для сопоставления опечаток и ошибок
from aiogram.types import Message
import spacy

from database.connect import get_product_from_db

# Инициализация NLP-модели для русского языка
nlp = spacy.load("ru_core_news_sm")

# Словарь, который хранит бренды и модели телефонов, включая русские версии
PRODUCT_CATALOG = {
    "apple": [
        {"en": "iphone 15 pro", "ru": "айфон 15 про"},
        {"en": "iphone 15", "ru": "айфон 15"},
        {"en": "iphone 14", "ru": "айфон 14"},
        {"en": "iphone 13", "ru": "айфон 13"},
        {"en": "iphone 12", "ru": "айфон 12"},
        {"en": "iphone se", "ru": "айфон se"}
    ],
    "samsung": [
        {"en": "galaxy s23", "ru": "галакси с23"},
        {"en": "galaxy s23 ultra", "ru": "галакси с23 ультра"},
        {"en": "galaxy z fold 5", "ru": "галакси z фолд 5"},
        {"en": "galaxy a54", "ru": "галакси а54"},
        {"en": "galaxy a34", "ru": "галакси а34"}
    ],
    "xiaomi": [
        {"en": "xiaomi 13", "ru": "сяоми 13"},
        {"en": "xiaomi 13 pro", "ru": "сяоми 13 про"},
        {"en": "redmi note 12", "ru": "редми ноут 12"},
        {"en": "redmi note 12 pro", "ru": "редми ноут 12 про"}
    ],
    # Добавьте больше брендов и моделей здесь
}

COMMON_PATTERNS = [
    r"сколько стоит", r"цена на", r"стоимость", r"цена", r"характеристики", r"сравни", r"сравнение", r"какая цена"
]

def clean_input(user_input):
    """
    Очищает пользовательский запрос от часто встречающихся фраз.
    """
    user_input = user_input.lower()
    for pattern in COMMON_PATTERNS:
        user_input = re.sub(pattern, '', user_input).strip()
    return user_input

def find_best_match(model_name, model_list):
    """
    Находит наиболее близкое соответствие модели в списке моделей.
    """
    choices = [model['en'] for model in model_list] + [model['ru'] for model in model_list]  # Список моделей на английском и русском
    best_match = process.extractOne(model_name, choices)
    return best_match[0] if best_match[1] >= 80 else None  # Вернуть только если совпадение >= 80%

def extract_model(user_input):
    """
    Извлекает модели смартфонов из запроса пользователя.
    """
    cleaned_input = clean_input(user_input)
    found_models = []

    # Проверяем, упоминается ли какая-либо модель из поддерживаемых брендов
    for brand, models in PRODUCT_CATALOG.items():
        for model in models:
            if model["en"] in cleaned_input or model["ru"] in cleaned_input:
                found_models.append((brand, model["en"]))  # Добавляем найденные модели в список

    return found_models  # Возвращаем список найденных моделей

async def get_phone_data(brand, product_name):
    """
    Асинхронная функция для получения информации о смартфоне.
    """
    product_data = await get_product_from_db(product_name)

    if "error" in product_data:
        return {"error": product_data["error"]}
    else:
        return {
            "product_name": product_name.title(),
            "price": product_data['price'],
            "description": product_data['description']
        }

async def process_user_input(user_input):
    """
    Обрабатывает ввод пользователя и возвращает информацию о телефоне.
    """
    found_models = extract_model(user_input)
    if not found_models:
        return "Не удалось распознать бренд или модель."

    responses = []  # Список для хранения ответов о моделях

    for brand, product_name in found_models:
        phone_data = await get_phone_data(brand, product_name)
        if "error" in phone_data:
            responses.append(phone_data["error"])
        else:
            response = f"<strong>Название:</strong> {phone_data['product_name']}\n" \
                       f"<strong>Цена:</strong> {phone_data['price']} рублей\n" \
                       f"<strong>Характеристики:</strong> {phone_data['description']}"
            responses.append(response)


    return "\n\n".join(responses)  # Объединяем все ответы в одно сообщение