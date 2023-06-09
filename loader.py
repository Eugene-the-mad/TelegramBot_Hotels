import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_data.config import config
from handlers import *
from utils.set_bot_commands import set_default_commands
from database import create_table
from aiogram import exceptions


async def main() -> None:
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher(storage=MemoryStorage())
    logging.basicConfig(level=logging.INFO)
    dp.include_routers(
        help.router,
        start.router,
        user_name.router,
        history.router,
        low.router,
        high.router,
        custom.router,
        echo.router
    )
    await create_table()
    try:
        await bot.set_my_commands(commands=set_default_commands())
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, polling_timeout=10)
    except exceptions.TelegramUnauthorizedError:
        print('Ошибка авторизации телеграмм бота. Введен неправильный токен. '
              'Проверьте еще раз введенный токен или запросите через BotFather '
              'новый токен.')
    else:
        print('Непредвиденная ошибка не сервере Telegram. Попробуйте еще раз или'
              'чуть позже.')
