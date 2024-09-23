from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message
from aiogram import types

async def open_profile(message: types.Message):

    buttons = [
        [types.InlineKeyboardButton(text="Редактировать профиль", callback_data='edit_profile')],
        [types.InlineKeyboardButton(text="Заказы", callback_data='orders')]
    ]

    kb = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)

    await message.answer('Профиль', reply_markup=kb)
