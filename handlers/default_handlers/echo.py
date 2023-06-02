from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from handlers.default_handlers.start import cmd_start

router = Router()


@router.message()
async def bot_echo(message: Message, state: FSMContext) -> None:
    """
    Эхо-функция. Срабатывает на любой текст пользователя, если он не выбрал режим работы бота.
    Запускает функцию cmd_start.
    """

    await cmd_start(message, state)
