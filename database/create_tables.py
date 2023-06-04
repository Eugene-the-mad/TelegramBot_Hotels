import aiosqlite as sq
from os import path


async def create_table() -> None:
    path_db = path.join(path.abspath(''), 'database/user.db')
    create_request = """
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        log_name TEXT NOT NULL,
        user_bot_id INTEGER NOT NULL,
        user_name TEXT NOT NULL)
    """
    async with sq.connect(path_db) as con:
        await con.execute(create_request)
        await con.commit()


async def create_table_actions() -> None:
    path_db = path.join(path.abspath(''), 'database/user.db')
    create_request = """
        CREATE TABLE IF NOT EXISTS users_action (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_bot_id TEXT INTEGER NOT NULL,
        date INTEGER NOT NULL,
        user_action TEXT NOT NULL)
    """
    async with sq.connect(path_db) as con:
        await con.execute(create_request)
        await con.commit()
