from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def num_person() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=str(i), callback_data='person_' + str(i)) for i in range(1, 5)],
            [InlineKeyboardButton(text=str(i), callback_data='person_' + str(i)) for i in range(5, 9)]
        ]
    )
    return kb
