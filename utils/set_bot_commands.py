from aiogram.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands() -> list[BotCommand]:
    return [
        BotCommand(command=com, description=desc) for com, desc in DEFAULT_COMMANDS
    ]
