from pydantic import BaseSettings, SecretStr
from dotenv import find_dotenv


class Settings(BaseSettings):
    bot_token: SecretStr
    rapid_api_key: SecretStr

    class Config:
        env_file = find_dotenv()
        env_file_encoding = 'utf-8'


if not find_dotenv():
    exit("Переменные окружения не загружены т.к. отсутствует файл .env")
else:
    config = Settings()

DEFAULT_COMMANDS = (
    ('/low', "поиск отелей по наименьшей цене"),
    ('/high', "поиск отелей по наибольшей цене"),
    ('/custom', "поиск отелей по диапазону цен"),
    ('/history', "отображение истории запросов пользователя"),
    ('/help', "описание команд данного бота")
)
