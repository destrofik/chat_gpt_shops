import os
import asyncpg
import aiopg
import psycopg2
from aiogram import types
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()


async def db_connect():
    connection = await asyncpg.connect(os.getenv('POSTGRESQL_URL'))



#Execute a statement to create a new table.
# await connection.execute('''
#         CREATE TABLE test1(
#             id serial PRIMARY KEY,
#             name text,
#             dob date
#             )''')

async def fio_insert(chat_id, name):
    connection = await asyncpg.connect(os.getenv('POSTGRESQL_URL'))
    await connection.execute("INSERT INTO users_register (tg_id, fio) VALUES ($1, $2)",  chat_id, str(name))
