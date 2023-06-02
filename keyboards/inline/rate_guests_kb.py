from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def rate_guests() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Хорошо 7+', callback_data='rate_guests:Хорошо 7+:35'),
                InlineKeyboardButton(text='Очень хорошо 8+', callback_data='rate_guests:Очень хорошо 8+:40'),
                InlineKeyboardButton(text='Отлично 9+', callback_data='rate_guests:Отлично 9+:45')
            ],
            [InlineKeyboardButton(text='Не учитывать оценку', callback_data='rate_guests:Не учитывать:not')]
        ]
    )
    return kb
