from aiogram import types


def type_meal_keyboard() -> types.InlineKeyboardMarkup:
    """
    Keyboard to select a meal type
    :return InlineKeyboardMarkup
    """
    button_breakfast = types.InlineKeyboardButton(text='Завтрак', callback_data="Завтрак")
    button_lunch = types.InlineKeyboardButton(text='Обед', callback_data="Обед")
    button_dinner = types.InlineKeyboardButton(text='Ужин', callback_data="Ужин")
    button_desserts = types.InlineKeyboardButton(text='Десерты', callback_data="Десерты")
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.insert(button_breakfast)
    keyboard.insert(button_lunch)
    keyboard.insert(button_dinner)
    keyboard.insert(button_desserts)
    return keyboard
