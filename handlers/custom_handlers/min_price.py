from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.filters import Text
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()


@router.message(Command('low'))
@router.message(Text('Наименьшая стоимость'))
async def send_welcome(message: types.Message):
    """
    Этот обработчик будет вызываться при нажатии на кнопку
    Наименьшая стоимость либо по команде /low
    """
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Минимальный"),
        types.KeyboardButton(text="Максимальный")
    )
    await message.answer("Выберите, какие показатели интересуют", reply_markup=builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выберите один из вариантов действий...'
    ))


@router.message(Text('Минимальный'))
async def send_welcome(message: types.Message):
    """
    Этот обработчик будет вызываться при получении команды /low
    """
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Пока ХЗ"),
        types.KeyboardButton(text="Так же ХЗ")
    )
    await message.answer("Выберите, какие показатели интересуют", reply_markup=builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выберите один из вариантов действий...'
    ))
