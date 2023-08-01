from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hlink

from config import BOT_TOKEN, DEFAULT_COMMANDS
from keyboards.start_keyboard import start_keyboard
from loguru import logger
from database.database import get_data_from_breakfast_table, get_data_from_desserts_table, get_data_from_lunch_table, \
    get_data_from_dinner_table, create_user

bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@logger.catch()
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    """
    Start function
    :param message: Object of message class
    :return: None
    """
    create_user(message)
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {start.__name__}")
    await message.answer("Здравствуйте! Я - бот для поиска рецептов. "
                         "Выберите <b>одну</b> из команд, чтобы начать работу.", reply_markup=start_keyboard())


@logger.catch()
@dp.message_handler(commands=["help"])
async def help_info(message: types.Message):
    """
    Function which helps you to choose a command
    :param message: Object of message class
    :return: None
    """
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду help")
    string = ""
    for name, description in DEFAULT_COMMANDS:
        string += f"<b>{name}</b> - {description}\n"
    await message.answer(string)


@logger.catch()
@dp.message_handler(commands=["breakfast"])
async def breakfast(message: types.Message) -> None:
    """
    Function for sending recipies for breakfast
    :param message: Object of message class
    :return: None
    """
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {breakfast.__name__}")
    queryset = get_data_from_breakfast_table(message=message, number=15)

    for items in queryset:
        message_structure = f"{hlink(items[1], items[5])}\nid: {items[0]}\n<b>Блюдо на</b>: " \
                           f"{items[2]}\n<b>Каллории</b>: {items[3]}\n<b>Время приготовления</b>: {items[4]}"
        await message.answer(message_structure)


@logger.catch()
@dp.message_handler(commands=["dinner"])
async def dinner(message: types.Message) -> None:
    """
    Function for sending recipies for dinner
    :param message: Object of message class
    :return: None
    """
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {dinner.__name__}")
    queryset = get_data_from_dinner_table(message=message, number=15)

    for items in queryset:
        message_structure = f"{hlink(items[1], items[5])}\nid: {items[0]}\n<b>Блюдо на</b>: " \
                           f"{items[2]}\n<b>Каллории</b>: {items[3]}\n<b>Время приготовления</b>: {items[4]}"
        await message.answer(message_structure)


@logger.catch()
@dp.message_handler(commands=["lunch"])
async def lunch(message: types.Message) -> None:
    """
    Function for sending recipies for lunch
    :param message: Object of message class
    :return: None
    """
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {lunch.__name__}")
    queryset = get_data_from_lunch_table(message=message, number=15)

    for items in queryset:
        message_structure = f"{hlink(items[1], items[5])}\nid: {items[0]}\n<b>Блюдо на</b>: " \
                           f"{items[2]}\n<b>Каллории</b>: {items[3]}\n<b>Время приготовления</b>: {items[4]}"
        await message.answer(message_structure)


@logger.catch()
@dp.message_handler(commands=["desserts"])
async def desserts(message: types.Message) -> None:
    """
    Function for sending recipies for desserts
    :param message: Object of message class
    :return: None
    """
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {desserts.__name__}")
    queryset = get_data_from_desserts_table(message=message, number=15)

    for items in queryset:
        message_structure = f"{hlink(items[1], items[5])}\nid: {items[0]}\n<b>Блюдо на</b>: " \
                           f"{items[2]}\n<b>Каллории</b>: {items[3]}\n<b>Время приготовления</b>: {items[4]}"
        await message.answer(message_structure)


def main() -> None:
    """
    Function which starts bot, start logs adn create a db
    :return: None
    """
    executor.start_polling(dp)


if __name__ == "__main__":
    logger.add('bot.log', format='{time} {level} {message}', level='DEBUG')
    logger.info('Бот вышел в онлайн...')
    main()
