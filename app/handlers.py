from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import datetime


from database.connect import db_connect, fio_insert
from app.generators import gpt
router = Router()

class Generate(StatesGroup):
    text = State()

class Registration(StatesGroup):
    entering_fio = State()
    entering_email = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Добро пожаловать! Чем могу помочь?')
    await state.clear()

@router.message(StateFilter(None), Command('Регистрация'))
async def registration(message: Message, state: FSMContext):
    await message.answer('Введите Ваше ФИО')
    await state.set_state(Registration.entering_fio)

@router.message(Registration.entering_fio, F.text)
async def insert_fio(message: Message, state: FSMContext):
    await fio_insert(message.from_user.id, message.text)
    await state.clear()


@router.message(Generate.text)
async def generate_error(message: Message):
    await message.answer('Подождите, ищу ответ на предыдущий вопрос...')

@router.message(StateFilter(None), F.text)
async def generate(message: Message, state: FSMContext):
    await state.set_state(Generate.text)
    response = await gpt(message.text)
    await message.answer(response.choices[0].message.content)
    await state.clear()

