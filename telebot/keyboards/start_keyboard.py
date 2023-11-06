from aiogram import types
from telebot.config import DEFAULT_COMMANDS


def start_keyboard() -> types.ReplyKeyboardMarkup:
    """
    Keyboard for main bot commands
    :return: ReplyKeyboardMarkup
    """
    start_buttons = [command[0] for command in DEFAULT_COMMANDS]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    return keyboard.add(*start_buttons)
