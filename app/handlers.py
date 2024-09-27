from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import datetime


from database.connect import db_connect, fio_insert, is_user_in_databse
from app.generators import gpt
from app.interface import main_keyboard, profile_keyboard
router = Router()

class Generate(StatesGroup):
    text = State()

class Registration(StatesGroup):
    check_user = State()
    entering_fio = State()
    entering_email = State()

class Interface(StatesGroup):
    open_profile = State()
    open_menu = State()



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


# МЕНЮ
@router.message(StateFilter(None), Command('menu'))
async def open_menu(message: Message, state: FSMContext):
    await message.answer('Запуск сообщения по команде /menu ', reply_markup=await main_keyboard(message.from_user.id))
    #await state.set_state(Interface.open_menu)



# ПРОФИЛЬ КЛИЕНТА:

# @router.callback_query(F.data == 'profile')
# async def show_profile_settings(call: CallbackQuery, state: FSMContext):
#     await call.answer('Открытие меню по команде Профиль ', reply_markup=await open_profile())

@router.message(lambda message: message.text == "Профиль")
async def open_profile_menu(message: Message, state: FSMContext):
    kb = await profile_keyboard()
    await message.answer("Профиль: Выберите действие", reply_markup=kb)
    await state.set_state(Interface.open_profile)

@router.message(Interface.open_profile, lambda message: message.text not in ['Редактировать профиль', 'Посмотреть профиль', 'Назад в меню', 'ХЗ'])
async def profile_warning(message: Message):
    await message.answer('Вернитесь в главное меню, если хотите написать боту')


# Обработчик для кнопки "Назад в меню", возвращает основную клавиатуру
@router.message(lambda message: message.text == "Назад в меню")
async def go_back_to_main_menu(message: Message):
    kb = await main_keyboard(message.from_user.id)
    await message.answer("Вы вернулись в главное меню", reply_markup=kb)

# Обработчик для других кнопок (например, "Настройки", "О нас")
@router.message(lambda message: message.text in ["Заказы", "О нас", "Контакты"])
async def handle_other_buttons(message: Message):
    if message.text == "Заказы":
        await message.answer("Заказы: Здесь вы можете посмотреть свои заказы.")
    elif message.text == "О нас":
        await message.answer("О нас: Мы команда разработчиков.")
    elif message.text == "Контакты":
        await message.answer("Контакты: Вы можете связаться с нами через почту.")





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

