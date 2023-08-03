from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink

from config import BOT_TOKEN, DEFAULT_COMMANDS
from keyboards.start_keyboard import start_keyboard
from loguru import logger
from database.database import get_data_from_breakfast_table, get_data_from_desserts_table, get_data_from_lunch_table, \
    get_data_from_dinner_table, create_user
from states import storage, StatesForCreate


bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


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
    await message.answer(f"Здравствуй, {message.from_user.full_name}! Я - бот для поиска рецептов. "
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


dict_for_created_recipe = dict()
alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')


@logger.catch()
@dp.message_handler(commands=["create"])
async def create_recipe(message: types.Message) -> None:
    """
    Funtion for creating recipies
    :params
        message - object of Message class
    :return
        none
    """
    await StatesForCreate.title.set()
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {create_recipe.__name__}")
    await message.answer("Приступим к созданию рецепта!\nВведите название блюда:")


@logger.catch()
@dp.message_handler(state=StatesForCreate.title)
async def set_title(message: types.Message, state: FSMContext) -> None:
    """
    Set type for created recipe
    :params
        message - object of Message class
    :return
        none
    """
    await StatesForCreate.type.set()
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {set_type.__name__}")
    if not alphabet.isdisjoint(message.text.lower()):

        async with state.proxy() as data:
            data["title"] = message.text

        dict_for_created_recipe["title"] = message.text
        await message.answer("Название принято, идем дальше. Из какого рациона дня блюдо? "
                             "<b>(завтрак, обед, ужин, десерты)</b>")
    else:
        dict_for_created_recipe.clear()
        await message.answer("Название должно содержать только буквы! Попробуйте еще раз "
                             "(выберите команду <b>заново</b>)")


@logger.catch()
@dp.message_handler(state=StatesForCreate.type)
async def set_type(message: types.Message, state: FSMContext) -> None:
    """
    Set type for created recipe
    :params
        message - object of Message class
    :return
        none
    """
    await StatesForCreate.time.set()
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {set_time.__name__}")

    if not alphabet.isdisjoint(message.text.lower()) and message.text.lower() in ["завтрак", "обед", "ужин", "десерты"]:

        async with state.proxy() as data:
            data["type"] = message.text

        dict_for_created_recipe["type"] = message.text
        await message.answer("Есть, идем дальше. Сколько времени требуется для приготовления блюда? "
                             "<b>(количество дней, если требуется:часов:минут)</b>")
    else:
        dict_for_created_recipe.clear()
        await message.answer("Тип рациона должен содержать только буквы! Попробуйте еще раз "
                             "(выберите команду <b>заново</b>)")


@logger.catch()
@dp.message_handler(state=StatesForCreate.time)
async def set_time(message: types.Message, state: FSMContext) -> None:
    """
    Set time for created recipe
    :params
        message - object of Message class
    :return
        none
    """
    await StatesForCreate.calories.set()
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {set_time.__name__}")
    split_message = message.text.split(":")
    string_message = ""

    for string in split_message:
        string_message += string

    if string_message.isdigit():

        async with state.proxy() as data:
            data["time"] = message.text

        dict_for_created_recipe["time"] = string_message
        StatesForCreate.calories.set()
        await message.answer("Время зафиксировано. Сколько каллорий весит блюдо? "
                             "<b>(число)</b>")
    else:
        dict_for_created_recipe.clear()
        await message.answer("Количество затраченного времени на приготовление должно содержать только цифры! "
                             "Попробуйте еще раз (выберите команду <b>заново</b>)")


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
