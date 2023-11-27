from aiogram import types
from aiogram.utils.callback_data import CallbackData


add_to_favorites_cd_walk = CallbackData("dun_w", "table_name", "pk")


def add_to_favorites(table_name: str, pk: int) -> types.InlineKeyboardMarkup:
    """
    Keyboard for adding recipies in favorites
    :params
        table_name - from which table is recipe
        pk - primary key of required recipe (to add it in favorites by pk)
    """
    button_add = types.InlineKeyboardButton(text='Добавить в избранные ❤️', callback_data=add_to_favorites_cd_walk.new(
        table_name=table_name, pk=pk
    ))
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.insert(button_add)
    return keyboard
