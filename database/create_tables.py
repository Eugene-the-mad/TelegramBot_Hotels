import sqlite3 as sq
from os import path


def create_table():
    path_db = path.join(path.abspath(''), 'database/user.db')
    with sq.connect(path_db) as con:
        cur = con.cursor()

        #cur.execute("DROP TABLE IF EXISTS users")  # Временное, УДАЛИТЬ!!!

        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_name TEXT NOT NULL,
            user_bot_id INTEGER NOT NULL,
            user_name TEXT NOT NULL)
            """)


create_table()


