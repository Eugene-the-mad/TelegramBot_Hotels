from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def next_canc(elem: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Продолжить', callback_data=elem + 'Продолжить')],
            [InlineKeyboardButton(text='Отмена', callback_data=elem + 'Отмена')],
        ]
    )
    return kb
