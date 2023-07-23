from aiogram import types


def start_keyboard() -> types.ReplyKeyboardMarkup:
    """
    Keyboard for main bot commands
    :return: ReplyKeyboardMarkup
    """
    start_buttons = ['/favorites', '/breakfast', '/lunch', '/dinner', '/desserts', '/create', '/help']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    return keyboard.add(*start_buttons)
