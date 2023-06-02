from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def select_kb(result: dict[str, str], val: str) -> InlineKeyboardMarkup:
    """ Функция, создающая инлайн-клавиатуру списком из переданных в неё значений. """
    kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=elem, callback_data=val + result[elem])]
                for elem in result.keys()
            ]
        )

    return kb
