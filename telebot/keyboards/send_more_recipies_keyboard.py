from aiogram import types
from aiogram.utils.callback_data import CallbackData


send_more_recipies_cd_walk = CallbackData("dun_w", "table_name", "answer")


def send_more_recipies_keyboard(table_name: str) -> types.InlineKeyboardMarkup:
    """
    Keyboard to ask about sending more data
    :params
        table_name - required table name for next callback function
    :return ReplyKeyboardMarkup
    """
    button_yes = types.InlineKeyboardButton(text='Да', callback_data=send_more_recipies_cd_walk.new(
        answer="Да", table_name=table_name
    ))
    button_no = types.InlineKeyboardButton(text='Нет', callback_data=send_more_recipies_cd_walk.new(
        answer="Нет", table_name=table_name
    ))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.insert(button_yes)
    keyboard.insert(button_no)
    return keyboard
