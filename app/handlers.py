from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.training import process_user_input
from database.connect import fio_insert, is_user_in_database, view_user_profile, edit_fio_profile, get_products, get_total_products
from app.generators import gpt
from app.interface import main_keyboard, profile_keyboard, call_manager_support, edit_keyboard, get_pagination_keyboard
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


class AssortmentState(StatesGroup):
    page = State()


class GPT(StatesGroup):
    GPT_enable = State()
    GPT_disable = State()


# СТАРТ

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Добро пожаловать! Я нейроассистент Hypell. Чем могу помочь?')
    await message.answer('Список быстрых команд:\nРегистрация - /registration\nКаталог - /assortment\n')
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


# Профиль -> Посмотреть профиль:

@router.message(lambda message: message.text == 'Посмотреть профиль')
async def open_view_user_profile(message: Message):
    user_profile = await view_user_profile(message.from_user.id)

    if user_profile:
        profile_info = f"ID: {user_profile['tg_id']}\nФИО: {user_profile['fio']}\nДата регистрации: {user_profile['registration_date']}\nАдрес доставки:"
        await message.answer(profile_info)
    else:
        await message.answer("Сначала Вам необходимо зарегистрироваться")


# Профиль -> Редактировать профиль:

@router.message(lambda message: message.text == 'Редактировать профиль')
async def open_edit_menu(message: Message):
    kb = await edit_keyboard()
    await message.answer("Профиль: Выберите действие", reply_markup=kb)


# Профиль -> Редактировать профиль -> Редактировать данные
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


# Пагинация данных
async def send_products(message: Message, page: int, state: FSMContext):
    limit = 3
    user_data = await state.get_data()

    # Получаем общее количество товаров один раз
    total_products = await get_total_products()
    total_pages = (total_products // limit) + (1 if total_products % limit else 0)

    # Кешируем текущую страницу и общее количество
    user_data['total_pages'] = total_pages
    await state.update_data(**user_data)

    # Получаем товары
    products = await get_products(page, limit)

    if not products:
        await message.answer("Нет доступных товаров.")
        return

    # Форматируем список товаров
    product_list = "\n\n".join([
        f"*Название:* `{product['name']}`\n"
        f"*Память:* `{product['memory']}Gb`\n"
        f"*Цвет:* `{product['color']}`\n"
        f"*Цена:* `{product['price']}₽`\n"
        f"*Страна:* `{product['country']}`\n"
        for product in products
    ])

    sent_message_id = user_data.get('sent_message_id')

    if sent_message_id is None:
        sent_message = await message.answer(
            text=f"{product_list}\n",
            parse_mode='MarkdownV2',
            reply_markup=get_pagination_keyboard(page, total_pages)
        )
        await state.update_data(sent_message_id=sent_message.message_id)
    else:
        await message.bot.edit_message_text(
            text=f"{product_list}\n",
            parse_mode='MarkdownV2',
            chat_id=message.chat.id,
            message_id=sent_message_id,
            reply_markup=get_pagination_keyboard(page, total_pages)
        )
    await state.update_data(page=page)


@router.message(Command('assortment'))
async def assortment_command(message: Message, state: FSMContext):
    # await state.set_state(AssortmentState.page)
    await send_products(message, page=1, state=state)


@router.callback_query()
async def handle_pagination(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    current_page = user_data.get('page', 1)
    total_pages = user_data.get('total_pages', 0)  # Получаем общее количество страниц из кеша

    if callback_query.data in ("prev_page", "next_page"):
        new_page = current_page - 1 if callback_query.data == "prev_page" else current_page + 1
        new_page = new_page if 1 <= new_page <= total_pages else (total_pages if new_page < 1 else 1)

        await send_products(callback_query.message, page=new_page, state=state)

    await callback_query.answer()  # Подтверждаем обработку колбека


# КОНТАКТЫ

@router.message(F.text == 'Контакты')
async def show_contacts(message: Message):
    await message.answer('Открытие контактов', reply_markup=await call_manager_support())


# Подключение GPT

@router.message(Generate.text)
async def generate_error(message: Message):
    await message.answer('Подождите, ищу ответ на предыдущий вопрос...')

# @router.message(StateFilter(None), F.text)
# async def generate(message: Message, state: FSMContext):
#     await state.set_state(Generate.text)
#     response = await gpt(message.text)
#     await message.answer(response.choices[0].message.content)
#     await state.clear()

exception_list = ['профиль', 'заказы', 'контакты', 'о нас', Command('registration'), Command('start'), Command('menu')]

@router.message(lambda message: message.text.lower() not in exception_list)
async def handle_message(message: Message):
    user_input = message.text
    result = await process_user_input(user_input)
    await message.answer(text=f"{result}\n", parse_mode="HTML")