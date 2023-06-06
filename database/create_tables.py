import aiosqlite as sq


async def create_table() -> None:
    create_request = [
        """
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        log_name TEXT NOT NULL,
        user_bot_id INTEGER NOT NULL,
        user_name TEXT NOT NULL)
        """,
        """
        CREATE TABLE IF NOT EXISTS users_action (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_bot_id INTEGER NOT NULL,
        date_in TEXT NOT NULL,
        user_action TEXT NOT NULL)
        """
    ]
    async with sq.connect('database/user.db') as con:
        for req in create_request:
            await con.execute(req)
        await con.commit()
