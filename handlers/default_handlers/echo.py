from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message

router = Router()


@router.message(Text)   # НУЖНО ДОДУМАТЬ
async def bot_echo(message: Message):
    await message.answer(
        f"Эхо без состояния или фильтра.\n"
        f"Сообщение: {message.text}"
    )

