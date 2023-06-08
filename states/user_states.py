from aiogram.filters.state import State, StatesGroup


class UserState(StatesGroup):
    name = State()
    cities = State()
    not_children = State()
    children = State()
    children_age = State()
    hotels = State()
    price_min = State()
    price_max = State()
    distance = State()
    history_select = State()
