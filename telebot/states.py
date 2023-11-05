from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State


storage = MemoryStorage()


class StatesForCreate(StatesGroup):
    title = State()
    type = State()
    time = State()
    calories = State()
    image = State()
    description = State()