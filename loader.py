import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_data.config import config
from handlers import *


async def main():
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
    # config.rapid_api_key.get_secret_value()
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        start.router,
        help.router,
        user_name.router,
        min_price.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, polling_timeout=10)
