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

async def get_product_from_db(product_name):
    """
    Извлекает информацию о продукте (цену и описание) из базы данных PostgreSQL.

    Args:
    - product_name: Название продукта (например, "iPhone 15").

    Returns:
    - Словарь с ценой и описанием продукта или сообщение об ошибке.
    """
    connection = await asyncpg.connect(os.getenv('POSTGRESQL_URL'))

    try:
        # Выполнение запроса к базе данных
        query = "SELECT price, description FROM products WHERE LOWER(name) = LOWER($1)"
        product_data = await connection.fetchrow(query, product_name)

        if product_data:
            return {"price": product_data['price'], "description": product_data['description']}
        else:
            #return {"price": ['Нет в наличии'], "description": product_data['description']}
            return {"error": f"Продукт <strong>{product_name}</strong> не найден в базе данных."}
    finally:
        await connection.close()