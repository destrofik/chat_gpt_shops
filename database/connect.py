import os
import asyncpg

from dotenv import load_dotenv


load_dotenv()

async def db_connect():
    connection = await asyncpg.connect(os.getenv('POSTGRESQL_URL'))


async def fio_insert(user_telegram_id: int, name):
    connection = await asyncpg.connect(os.getenv('POSTGRESQL_URL'))
    async with connection.transaction():
        await connection.execute("INSERT INTO users_register (tg_id, fio) VALUES ($1, $2)", user_telegram_id, str(name))
    connection.close()


async def is_user_in_database(user_id):
    connection = await asyncpg.connect(os.getenv('POSTGRESQL_URL'))
    exists = await connection.fetchval("SELECT 1 FROM users_register WHERE tg_id = $1", user_id)

    return exists


async def view_user_profile(user_telegram_id: int):
    connection = await asyncpg.connect(os.getenv('POSTGRESQL_URL'))
    user_profile = await connection.fetchrow(
        '''SELECT 
            tg_id, 
            fio, 
            TO_CHAR(registration_date, 'FMMonth DD, YYYY') AS registration_date 
        FROM users_register 
        WHERE tg_id = $1''', user_telegram_id)
    await connection.close()

    return user_profile


async def edit_fio_profile(user_telegram_id: int, name):
    connection = await asyncpg.connect(os.getenv('POSTGRESQL_URL'))
    async with connection.transaction():
        await connection.execute("UPDATE users_register SET fio = $2 WHERE tg_id = $1", user_telegram_id, str(name))
    await connection.close()


async def get_products(page: int, limit: int):
    offset = (page - 1) * limit
    connection = await asyncpg.connect(os.getenv('POSTGRESQL_URL'))

    products = await connection.fetch(f"""
        SELECT product_id, name, memory, color, price, country, description 
        FROM products 
        ORDER BY product_id 
        LIMIT {limit} OFFSET {offset}
    """)

    await connection.close()
    return products


async def get_total_products():
    connection = await asyncpg.connect(os.getenv('POSTGRESQL_URL'))
    total = await connection.fetchval("SELECT COUNT(*) FROM products")
    await connection.close()
    return total


# async def edit_address_profile(user_telegram_id: int):
#     connection = await asyncpg.connect(os.getenv('POSTGRESQL_URL'))
#     async with connection.transaction():
#     await connection.execute("UPDATE users_register SET address = $1",  str(address))
#     await connection.close()


# Функция для подключения к базе данных
async def get_smartphone_info(query: str):
    connection = await asyncpg.connect(os.getenv('POSTGRESQL_URL'))
    try:
        rows = await connection.fetch(query)
        return rows
    finally:
        await connection.close()

# Получение цены смартфона
async def get_smartphone_price(model_name):
    query = f"""
    SELECT price FROM products
    WHERE LOWER(name) = LOWER('{model_name}')
    """
    rows = await get_smartphone_info(query)

    if rows:
        return f"Цена {model_name}: {rows[0]['price']} рублей."
    else:
        return "К сожалению, я не нашел цену для указанной модели."


# Получение информации о смартфоне
async def get_smartphone_details(model_name):
    query = f"""
    SELECT name, memory, color, price, country, description FROM products
    WHERE LOWER(name) = LOWER('{model_name}')
    """
    rows = await get_smartphone_info(query)

    if rows:
        response = (f"*Модель:* `{rows[0]['name']}`\n"
                    f"*Память:* `{rows[0]['memory']} Gb`\n"
                    f"*Цвет:* `{rows[0]['color']}`\n"
                    f"*Цена:* `{rows[0]['price']} ₽`\n"
                    f"*Страна производитель:* `{rows[0]['country']}`\n"
                    f"*Описание:* `{rows[0]['description']}`")
    else:
        response = "К сожалению, я не нашел смартфон по вашему запросу."

    return response


# Сравнение смартфонов
async def compare_models(model1, model2):
    query = f"""
    SELECT name, memory, color, price, country, description FROM products
    WHERE LOWER(name) IN (LOWER('{model1}'), LOWER('{model2}'))
    """

    rows = await get_smartphone_info(query)

    if len(rows) == 2:
        response = (f"*Модель* `{rows[0]['name']}`:\n"
                    f"*Память:* `{rows[0]['memory']} Gb`\n"
                    f"*Цвет:* `{rows[0]['color']}`\n"
                    f"*Цена:* `{rows[0]['price']} ₽`\n"
                    f"*Страна:* `{rows[0]['country']}`\n"
                    f"*Описание:* `{rows[0]['description']}`\n\n"
                    f"*Модель* `{rows[1]['name']}:`\n"
                    f"*Память:* `{rows[1]['memory']} Gb`\n"
                    f"*Цвет:* `{rows[1]['color']}`\n"
                    f"*Цена:* `{rows[1]['price']} ₽`\n"
                    f"*Страна:* `{rows[1]['country']}`\n"
                    f"*Описание:* `{rows[1]['description']}.`")
    else:
        response = "Не удалось найти информацию о смартфонах для сравнения."

    return response
