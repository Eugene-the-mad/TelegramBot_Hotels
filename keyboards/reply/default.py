from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb = [
    [
        KeyboardButton(text='Наименьшая стоимость'),
        KeyboardButton(text='Наибольшая стоимость')
    ],
    [
        KeyboardButton(text='Поиск по параметрам'),
        KeyboardButton(text='История запросов')
    ],
    [KeyboardButton(text='Помощь')]
]

def_keyboard = ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберите один из вариантов действий...'
)
