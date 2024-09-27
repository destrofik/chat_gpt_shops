from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message, CallbackQuery
from aiogram import types
from aiogram.fsm.context import FSMContext

# async def open_profile(message: types.Message):
#
#     buttons = [
#         [types.InlineKeyboardButton(text="Редактировать профиль", callback_data='edit_profile')],
#         [types.InlineKeyboardButton(text="Заказы", callback_data='orders')]
#     ]
#
#     kb = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
#
#     await message.answer('Профиль', reply_markup=kb)

async def main_keyboard(user_telegram_id: int):

    kb_list = [
        [KeyboardButton(text="О нас", callback_data='about_us'), KeyboardButton(text="Профиль", callback_data='profile')],
        [KeyboardButton(text="Заказы", callback_data='orders'), KeyboardButton(text="Контакты", callback_data='manager')]
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
        [KeyboardButton(text='Посмотреть профиль', callback_data='show_profile'), KeyboardButton(text="Редактировать профиль", callback_data='edit_profile')],
        [KeyboardButton(text="ХЗ", callback_data='a'), KeyboardButton(text="ХЗ", callback_data='b')],
        [KeyboardButton(text="Назад в меню")]
    ]

    profile_kb = ReplyKeyboardMarkup(  # Corrected indentation here
        keyboard=profile_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Профиль:"
    )

    return profile_kb
