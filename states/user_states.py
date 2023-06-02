from aiogram.filters.state import State, StatesGroup


class UserState(StatesGroup):
    name = State()
    cities = State()
    hotels = State()
    price_min = State()
    price_max = State()
    distance = State()
