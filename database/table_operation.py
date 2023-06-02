import sqlite3 as sq
from os import path
from typing import Optional


def check_name(user_id: int) -> Optional[tuple[str]]:
    path_db = path.join(path.abspath(''), 'database/user.db')
    with sq.connect(path_db) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT user_name FROM users WHERE user_bot_id == {user_id}""")
        result = cur.fetchone()
        if result:
            return result
        else:
            return result


def insert_user_data(data_user: tuple[str, int, str]) -> None:
    path_db = path.join(path.abspath(''), 'database/user.db')
    with sq.connect(path_db) as con:
        cur = con.cursor()
        cur.execute("""
        INSERT INTO users(log_name, user_bot_id, user_name) 
        VALUES(?, ?, ?)  
        """, data_user)
