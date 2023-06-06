from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def history_selection() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Сегодня', callback_data='history:today'),
                InlineKeyboardButton(text='Вчера', callback_data='history:yesterday'),
                InlineKeyboardButton(text='Указать дату', callback_data='history:custom')
            ],
            [InlineKeyboardButton(text='За всё время', callback_data='history:all')]
        ]
    )
    return kb
