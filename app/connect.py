import os
import asyncpg
import aiopg
import psycopg2
from aiogram import types
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

dsn = os.getenv('POSTGRESQL_URL')
# dsn = 'postgresql://postgres:Ronaldo9399@localhost:5432/chat_bot'


'''
class Database:
    def __init__(self, dsn):
        self.dsn = dsn
        self.pool = None

    async def init(self):
        self.pool = await asyncpg.create_pool(dsn=self.dsn)

    async def fetch_user_data(self, user_id):
        async with self.pool.acquire() as connection:
            result = await connection.fetch('SELECT * FROM users_register WHERE user_id = $1', user_id)
            return result

    async def close(self):
        await self.pool.close()

async def db_user_insert(message):
    async with aiopg.create_pool(dsn) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute('INSERT INTO users_register (fio) VALUES (%s)', message)
                print("Вы успешно зарегестрированы!")'''



'''async def on_startup(db):
    # Инициализация базы данных
    await db.init()
async def on_shutdown(db):
    # Закрытие базы данных
    await db.close()
async def handle_start(message: types.Message):
    user_id = message.from_user.id
    user_data = await db.fetch_user_data(user_id)
    await message.answer(f"Данные пользователя: {user_data}")'''


