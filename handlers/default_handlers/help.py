from aiogram import types, Router
from aiogram.filters import Text
from aiogram.filters.command import Command
from config_data.config import DEFAULT_COMMANDS

router = Router()


@router.message(Command('help'))
@router.message(Text('Помощь'))
async def cmd_help(message: types.Message) -> None:
    """
    Этот обработчик будет вызываться при нажатии на кнопку
    Помощь либо по команде /help. Имеет приоритет над остальными командами бота.
    Выводит информацию по командам бота.
    """
    help_com = "\n".join([f'{com_name} - {com_sur}' for com_name, com_sur in DEFAULT_COMMANDS])
    await message.answer(
        f'<u><b>Список команд бота EugeneBot:</b></u>\n{help_com}'
    )
