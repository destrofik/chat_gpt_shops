from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.types import Message, CallbackQuery
from aiogram import types
from aiogram.fsm.context import FSMContext


async def main_keyboard():

    kb_list = [
        [KeyboardButton(text="О нас"), KeyboardButton(text="Профиль")],
        [KeyboardButton(text="Заказы"), KeyboardButton(text="Контакты")]
    ]

    kb = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )

    return kb



async def profile_keyboard():

    profile_list = [
        [KeyboardButton(text='Посмотреть профиль'), KeyboardButton(text="Редактировать профиль")],
        [KeyboardButton(text="В главное меню")]
    ]

    profile_kb = ReplyKeyboardMarkup(  # Corrected indentation here
        keyboard=profile_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Профиль:"
    )

    return profile_kb

async def edit_keyboard():

    edit_list = [
        [KeyboardButton(text='ФИО'), KeyboardButton(text="Адрес доставки")],
        [KeyboardButton(text="Назад"), KeyboardButton(text="В главное меню")]
    ]

    edit_kb = ReplyKeyboardMarkup(  # Corrected indentation here
        keyboard=edit_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Редактировать"
    )

    return edit_kb


async def call_manager_support():
    buttons_list = [
        [InlineKeyboardButton(text="Менеджер", url='https://t.me/vyacheslav_bikir')],
        [InlineKeyboardButton(text="Тех. поддержка", url='https://t.me/destrofikk'), InlineKeyboardButton(text="Тех. поддержка", url='https://t.me/Daniil_2004')],
        [InlineKeyboardButton(text="Hypell", web_app=WebAppInfo(url='https://vk.com/hypell_ru'))]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons_list, row_width=1)

    return keyboard