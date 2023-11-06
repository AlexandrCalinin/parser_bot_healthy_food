import os.path

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink

from config import BOT_TOKEN, DEFAULT_COMMANDS
from keyboards.start_keyboard import start_keyboard
from loguru import logger
from database.database import get_data_from_breakfast_table, get_data_from_desserts_table, get_data_from_lunch_table, \
    get_data_from_dinner_table, create_user, send_data_from_recipe_to_database, get_created_history
from states import storage, StatesForCreate

bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')


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
    await message.answer(f"Здравствуй, {message.from_user.full_name}! 🙋\nЯ - бот для поиска рецептов. 🔥\n"
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
        string += f"➡️<b>{name}</b> - {description}\n"
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
        message_structure = f"{hlink(items[1], items[5])} 😱\n🆔 id: {items[0]}\n<b>🍽 Блюдо на</b>: " \
                            f"{items[2]}\n<b>🍔 Каллории</b>: {items[3]}\n<b>⏳ Время приготовления</b>: {items[4]}"
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
        message_structure = f"{hlink(items[1], items[5])} 😱\n🆔 id: {items[0]}\n<b>🍽 Блюдо на</b>: " \
                            f"{items[2]}\n<b>🍔 Каллории</b>: {items[3]}\n<b>⏳ Время приготовления</b>: {items[4]}"
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
        message_structure = f"{hlink(items[1], items[5])} 😱\n🆔 id: {items[0]}\n<b>🍽 Блюдо на</b>: " \
                            f"{items[2]}\n<b>🍔 Каллории</b>: {items[3]}\n<b>⏳ Время приготовления</b>: {items[4]}"
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
        message_structure = f"{hlink(items[1], items[5])} 😱\n🆔 id: {items[0]}\n<b>🍽 Блюдо на</b>: " \
                            f"{items[2]}\n<b>🍔 Каллории</b>: {items[3]}\n<b>⏳ Время приготовления</b>: {items[4]}"
        await message.answer(message_structure)


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
    await message.answer("Приступим к созданию рецепта! 🆕\nВведите название блюда 🍽:")


@logger.catch()
@dp.message_handler(state=StatesForCreate.title)
async def set_title(message: types.Message, state: FSMContext) -> None:
    """
    Set type for created recipe
    :params
        message - object of Message class
        state - object of FSM
    :return
        none
    """
    await StatesForCreate.type.set()
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {set_type.__name__}")
    if not alphabet.isdisjoint(message.text.lower()):

        async with state.proxy() as data:
            data["title"] = message.text

        await message.answer("✅ Название принято, идем дальше. Из какого рациона дня блюдо?\n"
                             "<b>(завтрак, обед, ужин, десерты)</b>")
    else:
        await message.answer("Название должно содержать только буквы! ❌\n"
                             "Попробуйте еще раз (выберите команду <b>заново</b>)! 🔄")


@logger.catch()
@dp.message_handler(state=StatesForCreate.type)
async def set_type(message: types.Message, state: FSMContext) -> None:
    """
    Set type for created recipe
    :params
        message - object of Message class
        state - object of FSM
    :return
        none
    """
    await StatesForCreate.time.set()
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {set_time.__name__}")

    if not alphabet.isdisjoint(message.text.lower()) and message.text.lower() in ["завтрак", "обед", "ужин", "десерты"]:

        async with state.proxy() as data:
            data["type"] = message.text

        await message.answer("✅ Есть, идем дальше. Сколько времени требуется для приготовления блюда?\n"
                             "<b>(Пример: 3 д 2 ч 1 мин)</b>")
    else:
        await message.answer("Тип рациона должен содержать только буквы! ❌\n"
                             "Воспользуйтесь примером и попробуйте еще раз (выберите команду <b>заново</b>)! 🔄")


@logger.catch()
@dp.message_handler(state=StatesForCreate.time)
async def set_time(message: types.Message, state: FSMContext) -> None:
    """
    Set time for created recipe
    :params
        message - object of Message class
        state - object of FSM
    :return
        none
    """
    await StatesForCreate.calories.set()
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {set_time.__name__}")

    if message.text.replace(" ", "").isalnum():

        async with state.proxy() as data:
            data["time"] = message.text

        await message.answer("✅ Время зафиксировано. Сколько каллорий весит блюдо?\n"
                             "<b>(Пример: 123 ккал)</b>")
    else:
        await message.answer("Количество затраченного времени должно содержать только цифры и буквы! ❌\n"
                             "Воспользуйтесь примером и попробуйте еще раз (выберите команду <b>заново</b>)! 🔄")


@logger.catch()
@dp.message_handler(state=StatesForCreate.calories)
async def set_calories(message: types.Message, state: FSMContext) -> None:
    """
    Set calories for created recipe
    :params
        message - object of Message class
        state - object of FSM
    :return
        none
    """
    await StatesForCreate.description.set()
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {set_calories.__name__}")

    if message.text.replace(" ", "").isalnum():

        async with state.proxy() as data:
            data["calories"] = message.text

        await message.answer("Эх, постоянная борьба с каллориями... 😔\n"
                             "⏭ Опишите вкратце этапы приготовления. \n"
                             "Пример: (1. Разбить яйцо. 2. Добавить муку ...)")
    else:
        await message.answer("Количество каллорий должно содержать только буквы и цифры. ❌\n "
                             "Воспользуйтесь примером и попробуйте еще раз (выберите команду <b>заново</b>)! 🔄")


@logger.catch()
@dp.message_handler(state=StatesForCreate.description)
async def set_description(message: types.Message, state: FSMContext) -> None:
    """
    Set description for created recipe
    :params
        message - object of Message class
        state - object of FSM
    :return
        none
    """
    await StatesForCreate.image.set()
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {set_photo.__name__}")

    async with state.proxy() as data:
        data["description"] = message.text

    await message.answer("✅ Принято, последний шаг!\n"
                         "Пришлите фотографию для лучшего отображения 🖼")


@logger.catch()
@dp.message_handler(state=StatesForCreate.image, content_types=['photo'])
async def set_photo(message: types.Message, state: FSMContext) -> None:
    """
    Set calories for created recipe
    :params
        message - object of Message class
        state - object of FSM
    :return
        none
    """
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {set_photo.__name__}")

    async with state.proxy() as data:
        photo_url = os.path.abspath(
            os.path.join('images', f"{data['title']}_{message.from_user.id}.png"))
        await message.photo[-1].download(destination_file=photo_url)
        send_data_from_recipe_to_database(message=message, title=data['title'], type_meal=data['type'],
                                          calories=data['calories'],
                                          time=data['time'], description=data['description'], photo=photo_url)
        photo_lsd = open(photo_url, 'rb')
        await bot.send_photo(message.chat.id, photo=photo_lsd, caption=f"Название: {data['title']}😱\n"
                                                                       f"<b>🍽 Блюдо на</b>: {data['type']}\n"
                                                                       f"<b>🍔 Каллории</b>: {data['calories']}\n"
                                                                       f"<b>⏳ Время приготовления</b>: {data['time']}\n"
                                                                       f"<b>Описание</b>: {data['description']}")


@logger.catch()
@dp.message_handler(commands=['create_history'])
async def create_history(message: types.Message) -> None:
    """
    Show history if created products
    :params
        message - object of Message class
    :return
        none
    """
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {create_history.__name__}")
    query = get_created_history(message=message)

    if not query:
        await message.answer("Увы, вы еще не создали ни одного рецепта.\n"
                             "Попробуйте <strong>создать</strong>, используя команду /create или "
                             "выберите <strong>другую</strong> команду из /help")
    else:
        for indexes in query:
            photo_lsd = open(indexes[5], 'rb')
            await bot.send_photo(message.chat.id,
                                 photo=photo_lsd,
                                 caption=f"Название: {indexes[0]}😱\n"
                                         f"<b>🍽 Блюдо на</b>: {indexes[1]}\n"
                                         f"<b>🍔 Калории</b>: {indexes[2]}\n"
                                         f"<b>⏳ Время приготовления</b>: {indexes[3]}\n"
                                         f"<b>Описание</b>: {indexes[4]}")


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
