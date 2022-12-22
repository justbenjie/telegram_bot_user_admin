from aiogram.dispatcher.filters.state import State, StatesGroup


class User(StatesGroup):
    name = State()
    phone = State()
    gender = State()
