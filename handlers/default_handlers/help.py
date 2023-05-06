from aiogram import types, Router
from aiogram.filters import Text
from aiogram.filters.command import Command
from keyboards.reply import def_keyboard
from config_data.config import DEFAULT_COMMANDS

router = Router()


@router.message(Command('help'))
@router.message(Text('Помощь'))
async def cmd_help(message: types.Message):
    help_com = "\n".join([f'{com_name} - {com_sur}' for com_name, com_sur in DEFAULT_COMMANDS])
    await message.answer(
        f'<u><b>Список команд бота EugeneBot:</b></u>\n{help_com}',
        reply_markup=def_keyboard,
        input_field_placeholder='Выберите один из вариантов действий...'
    )




