from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def y_n(param: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Да', callback_data=param + 'Да')],
            [InlineKeyboardButton(text='Нет', callback_data=param + 'Нет')],
        ]
    )
    return kb
