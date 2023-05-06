from aiogram.filters.state import State, StatesGroup


class UserState(StatesGroup):
    name = State()
