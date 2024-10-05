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
        await connection.execute("UPDATE users_register SET fio = $2 WHERE tg_id = $1",  user_telegram_id, str(name))
    await connection.close()


# async def edit_address_profile(user_telegram_id: int):
#     connection = await asyncpg.connect(os.getenv('POSTGRESQL_URL'))
#     async with connection.transaction():
#     await connection.execute("UPDATE users_register SET address = $1",  str(address))
#     await connection.close()

