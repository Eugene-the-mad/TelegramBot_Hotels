from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb = [
    [
        KeyboardButton(text='Наименьшая стоимость'),
        KeyboardButton(text='Наибольшая стоимость')
    ],
    [
        KeyboardButton(text='Диапазон значений'),
        KeyboardButton(text='История запросов')
    ],
    [KeyboardButton(text='Помощь')]
]

def_keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
