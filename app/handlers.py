from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import datetime


from database.connect import db_connect, fio_insert, is_user_in_databse
from app.generators import gpt
from app.interface import open_profile
router = Router()

class Generate(StatesGroup):
    text = State()

class Registration(StatesGroup):
    check_user = State()
    entering_fio = State()
    entering_email = State()

class Interface(StatesGroup):
    open_profile = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Добро пожаловать! Я нейроассистент Hypell. Чем могу помочь?')
    await message.answer('Список быстрых команд:\nРегистрация - /registration\nПерейти в профиль - /profile\nСвязь с менеджером - /manager')
    await state.clear()


# ПЕРВОНАЧАЛЬНАЯ РЕГИСТРАЦИЯ:
@router.message(StateFilter(None), Command('registration'))
async def registration(message: Message, state: FSMContext):
    await state.set_state(Registration.check_user)
    exists = await is_user_in_databse(message.from_user.id)

    if exists:
        await message.answer('Вы уже зарегистрированы!')
        await state.clear()
    else:
        await message.answer('Введите Ваше ФИО')
        await state.set_state(Registration.entering_fio)

@router.message(Registration.entering_fio, F.text)
async def insert_fio(message: Message, state: FSMContext):
    await fio_insert(message.from_user.id, message.text)
    await message.answer('Вы успешно зарегистрированы!')
    await state.clear()


# ПРОФИЛЬ КЛИЕНТА:
@router.message(StateFilter(None), Command('profile'))
async def show_profile(message: Message, state: FSMContext):
    await open_profile(message)
    await state.set_state(Interface.open_profile)

@router.message(Interface.open_profile, F.text)
async def profile(message: Message, state: FSMContext):
    if F.text == 'Заказы': pass
    elif F.text == 'Редактировать профиль': pass



# Подключение GPT
@router.message(Generate.text)
async def generate_error(message: Message):
    await message.answer('Подождите, ищу ответ на предыдущий вопрос...')

@router.message(StateFilter(None), F.text)
async def generate(message: Message, state: FSMContext):
    await state.set_state(Generate.text)
    response = await gpt(message.text)
    await message.answer(response.choices[0].message.content)
    await state.clear()

