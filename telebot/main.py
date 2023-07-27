from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, DEFAULT_COMMANDS
from keyboards.start_keyboard import start_keyboard
from loguru import logger
from database.database import *


bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    """
    Start function
    :param message: Object of message class
    :return: None
    """
    await message.answer("Здравствуйте! Я - бот для поиска рецептов. "
                         "Выберите <b>одну</b> из команд, чтобы начать работу.", reply_markup=start_keyboard())


@dp.message_handler(commands=["help"])
async def help_info(message: types.Message):
    """
    Function which helps you to choose a command
    :param message: Object of message class
    :return: None
    """
    string = ""
    for name, description in DEFAULT_COMMANDS:
        string += f"<b>{name}</b> - {description}\n"
    await message.answer(string)


@dp.message_handler(commands=["breakfast"])
async def breakfast(message: types.Message) -> None:
    """
    Function for sending recipies for breakfast
    :param message: Object of message class
    :return: None
    """
    await message.answer("FAS")


def main() -> None:
    """
    Function which starts bot, start logs adn create a db
    :return: None
    """
    executor.start_polling(dp)


if __name__ == "__main__":
    logger.add('bot.log', format='{time} {level} {message}', level='DEBUG')
    logger.info('Бот вышел в онлайн...')
    with db:
        db.create_tables([User, Recipies, Favorites])
    main()
