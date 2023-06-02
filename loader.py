import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_data.config import config
from handlers import *
from utils.set_bot_commands import set_default_commands


async def main() -> None:
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        help.router,
        start.router,
        user_name.router,
        low.router,
        high.router,
        custom.router,
        echo.router
    )
    await bot.set_my_commands(commands=set_default_commands())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, polling_timeout=10)
