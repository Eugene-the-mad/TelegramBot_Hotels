import aiosqlite as sq
from os import path
from typing import Optional
from datetime import datetime


async def check_name(user_id: int) -> Optional[tuple[str]]:
    path_db = path.join(path.abspath(''), 'database/user.db')
    select_request = f"""
        SELECT user_name 
        FROM users 
        WHERE user_bot_id == {user_id}
    """
    async with sq.connect(path_db) as con:
        async with con.execute(select_request) as a_result:
            result = await a_result.fetchone()
            if result:
                return result
            else:
                return result


async def insert_user_data(data_user: tuple[str, int, str]) -> None:
    path_db = path.join(path.abspath(''), 'database/user.db')
    insert_request = """
        INSERT INTO users(log_name, user_bot_id, user_name) 
        VALUES(?, ?, ?)  
    """
    async with sq.connect(path_db) as con:
        await con.execute(insert_request, data_user)
        await con.commit()


async def insert_user_action(data_user: tuple[str, int, str]) -> None:
    path_db = path.join(path.abspath(''), 'database/user.db')
    insert_request = """
        INSERT INTO users_action(log_name, user_bot_id, user_name) 
        VALUES(?, ?, ?)  
    """
    async with sq.connect(path_db) as con:
        await con.execute(insert_request, data_user)
        await con.commit()
