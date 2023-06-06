import aiosqlite as sq
from typing import Optional, Any
from datetime import datetime, timedelta, date



async def check_name(user_id: int) -> Optional[tuple[str]]:
    path_db = 'database/user.db'
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
    path_db = 'database/user.db'
    insert_request = """
        INSERT INTO users(log_name, user_bot_id, user_name) 
        VALUES(?, ?, ?)  
    """
    async with sq.connect(path_db) as con:
        await con.execute(insert_request, data_user)
        await con.commit()


async def insert_user_action(data_user: tuple[int, Any, str]) -> None:
    path_db = 'database/user.db'
    insert_request = """
        INSERT INTO users_action(user_bot_id, date_in, user_action) 
        VALUES(?, ?, ?)  
    """
    async with sq.connect(path_db) as con:
        await con.execute(insert_request, data_user)
        await con.commit()


async def search_user_action(user_id: int, param: str, date_user: datetime = None) -> Optional[str]:
    path_db = 'database/user.db'
    date_search = ''

    if param == 'today':
        date_search = date.today()

    elif param == 'yesterday':
        date_search = date.today() - timedelta(days=1)

    elif param == 'custom':
        date_search = date_user.date()

    values = (date_search, user_id)
    insert_request = """
                        SELECT time(date_in), user_action 
                        FROM users_action
                        WHERE date(date_in) = date(?) AND user_bot_id == (?)
                    """

    if param == 'all':
        values = (user_id,)
        insert_request = """
                            SELECT datetime(date_in), user_action 
                            FROM users_action
                            WHERE user_bot_id == (?)
                         """

    async with sq.connect(path_db) as con:
        async with con.execute(insert_request, values) as result_:
            result = await result_.fetchall()
            if result:
                if date_search:
                    result_ = '\n'.join('<b>' + elem[0] + '</b>\t\t' + elem[1] for elem in result)
                    return f'<b>Дата: {date_search}</b>\n' + result_

                date_day = ''
                all_action = list()
                for elem in result:
                    if not date_day:
                        date_day = elem[0][:10]
                        all_action.append(f'\t\t\t<b>{date_day}</b>')
                    if date_day == elem[0][:10]:
                        all_action.append('\t\t'.join([elem[0][11:], elem[1]]))
                    else:
                        date_day = elem[0][:10]
                        all_action.append(f'\n\t\t\t<b>{date_day}</b>')
                        all_action.append('\t\t'.join([elem[0][11:], elem[1]]))

                return '<b>Запросы за всё время:</b>\n' + '\n'.join(all_action)

            return None
