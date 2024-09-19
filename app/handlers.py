from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

#from database.connect import Database
#from database.connect import db_user_insert
from app.generators import gpt
router = Router()

class Generate(StatesGroup):
    text = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Добро пожаловать! Чем могу помочь?')
    await state.clear()

'''@router.message(Command('юзеры'))
async def show_user(message: Message, state: FSMContext):
    await message.answer('Введите user_id')
    await Database.fetch_user_data(float(message.text))

@router.message(Command('Регистрация'))
async def generate_fio(message: Message, state: FSMContext):
    await message.answer('Введите Ваше ФИО')
    res = message.text
    await db_user_insert(res)
    await state.clear()'''

@router.message(Generate.text)
async def generate_error(message: Message):
    await message.answer('Подождите, ищу ответ на предыдущий вопрос...')

@router.message(F.text)
async def generate(message: Message, state: FSMContext):
    await state.set_state(Generate.text)
    response = await gpt(message.text)
    await message.answer(response.choices[0].message.content)
    await state.clear()


'''

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    conn = await get_db_connection()
    async with conn.acquire() as connection:
        async with connection.cursor() as cursor:
            # Создание таблицы, если она не существует
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS info (
                    id BIGINT PRIMARY KEY
                )
            """)

            people_id = message.chat.id

            # Проверка, существует ли уже пользователь в базе данных
            await cursor.execute("SELECT id FROM info WHERE id = %s", (people_id,))
            data = await cursor.fetchone()

            if data is None:
                # Добавление идентификатора пользователя, если он не найден
                await cursor.execute("INSERT INTO info (id) VALUES (%s);", (people_id,))
                await connection.commit()
                await message.answer('Вы успешно зарегистрированы!')
            else:
                await message.answer('Вы уже зарегистрированы')

    # Отправка приветственного сообщения
    await message.answer('Добро пожаловать! Чем могу помочь?')

    # Очистка состояния
    await state.clear()
'''
