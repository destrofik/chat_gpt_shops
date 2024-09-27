import os
import asyncpg
import aiopg
import psycopg2
from aiogram import types

from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext


load_dotenv()

async def db_connect():
    connection = await asyncpg.connect(os.getenv('POSTGRESQL_URL'))


async def fio_insert(user_telegram_id: int, name):
    connection = await asyncpg.connect(os.getenv('POSTGRESQL_URL'))
    async with connection.transaction():
        await connection.execute("INSERT INTO users_register (tg_id, fio) VALUES ($1, $2)",  user_telegram_id, str(name))
    connection.close()

async def is_user_in_databse(user_id):
    connection = await asyncpg.connect(os.getenv('POSTGRESQL_URL'))
    exists = await connection.fetchval("SELECT 1 FROM users_register WHERE tg_id = $1", user_id)

    return exists



