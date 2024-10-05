from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


from database.connect import fio_insert, is_user_in_database, view_user_profile, edit_fio_profile
from app.generators import gpt
from app.interface import main_keyboard, profile_keyboard, call_manager_support, edit_keyboard
router = Router()

class Generate(StatesGroup):
    text = State()

class Registration(StatesGroup):
    check_user = State()
    entering_fio = State()
    entering_email = State()

class Interface(StatesGroup):
    open_profile = State()
    edit_profile = State()
    open_menu = State()
    edit_fio = State()

class GPT(StatesGroup):
    GPT_enable = State()
    GPT_disable = State()

# СТАРТ

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Добро пожаловать! Я нейроассистент Hypell. Чем могу помочь?')
    await message.answer('Список быстрых команд:\nРегистрация - /registration\nПерейти в профиль - /profile\nСвязь с менеджером - /manager')
    await state.clear()


# ПЕРВОНАЧАЛЬНАЯ РЕГИСТРАЦИЯ:

@router.message(StateFilter(None), Command('registration'))
async def registration(message: Message, state: FSMContext):
    await state.set_state(Registration.check_user)
    exists = await is_user_in_database(message.from_user.id)

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
async def open_menu(message: Message):
    await message.answer('Запуск сообщения по команде /menu ', reply_markup=await main_keyboard())



# ПРОФИЛЬ:

@router.message(lambda message: message.text == "Профиль")
async def open_profile_menu(message: Message):
    kb = await profile_keyboard()
    await message.answer("Профиль: Выберите действие", reply_markup=kb)


#Профиль -> Посмотреть профиль:

@router.message(lambda message: message.text == 'Посмотреть профиль')
async def open_view_user_profile(message: Message):
    user_profile = await view_user_profile(message.from_user.id)

    if user_profile:
        profile_info = f"ID: {user_profile['tg_id']}\nФИО: {user_profile['fio']}\nДата регистрации: {user_profile['registration_date']}\nАдрес доставки:"
        await message.answer(profile_info)
    else:
        await message.answer("Сначала Вам необходимо зарегистрироваться")

#Профиль -> Редактировать профиль:

@router.message(lambda message: message.text == 'Редактировать профиль')
async def open_edit_menu(message: Message):
    kb = await edit_keyboard()
    await message.answer("Профиль: Выберите действие", reply_markup=kb)


#Профиль -> Редактировать профиль -> Редактировать данные
@router.message(lambda message: message.text == 'ФИО')
async def open_edit_user_profile(message: Message, state: FSMContext):
    await message.answer('Введите новое ФИО')
    await state.set_state(Interface.edit_fio)

@router.message(Interface.edit_fio, F.text)
async def open_edit_user_profile(message: Message, state: FSMContext):
    await edit_fio_profile(message.from_user.id, message.text)
    await message.answer('Вы успешно изменили ФИО!')
    await state.clear()

# Профиль -> Назад в меню
# Обработчик для кнопки "Назад в меню", возвращает основную клавиатуру
@router.message(lambda message: message.text == "В главное меню")
async def go_back_to_main_menu(message: Message):
    await message.answer("Вы вернулись в главное меню", reply_markup=await main_keyboard())

# Профиль -> Редактировать профиль -> Назад в профиль
# Обработчик для кнопки "Назад в меню", возвращает основную клавиатуру
@router.message(lambda message: message.text == "Назад")
async def go_back_to_profile_menu(message: Message):
    await message.answer("Вы вернулись в Профиль", reply_markup=await profile_keyboard())



# КОНТАКТЫ

@router.message(F.text == 'Контакты')
async def show_contacts(message: Message):
    await message.answer('Открытие контактов', reply_markup=await call_manager_support())



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

