import os.path
import re
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink

from config import BOT_TOKEN, DEFAULT_COMMANDS
from keyboards.start_keyboard import start_keyboard
from keyboards.send_more_recipies_keyboard import send_more_recipies_keyboard, send_more_recipies_cd_walk
from keyboards.type_meal_keyboard import type_meal_keyboard
from keyboards.add_to_favorites import add_to_favorites, add_to_favorites_cd_walk
from loguru import logger
from database.database import (create_user, send_data_from_recipe_to_database, get_created_history,
                               get_data_from_table_in_range, add_recipe_to_favorites_table_db)
from states import storage, StatesForCreate

bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
regex = "^[a-zA-Zа-яА-ЯёЁ]+$"
pattern = re.compile(regex)
counter_for_breakfast = 0
counter_for_dinner = 0
counter_for_lunch = 0
counter_for_desserts = 0


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
                         "Выберите команду /help, чтобы увидеть справочник по всем командам для более комфортного и "
                         "понятного использования ☺️",
                         reply_markup=start_keyboard())


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


async def send_more_recipies(message: types.Message, table_name: str, quantity_range: int = 0) -> None:
    """
    Function which get data from required table recipies in a specific range
    :params
        message - Object of message class
        quantity_range - range of required pk
        table_name - name of required table
    :return
        None
    """
    try:
        queryset = get_data_from_table_in_range(message=message, number=quantity_range * 15, table_name=table_name)
        for items in queryset:
            message_structure = f"{hlink(items[1], items[5])} 😱\n🆔 id: {items[0]}\n<b>🍽 Блюдо на</b>: " \
                                f"{items[2]}\n<b>🍔 Калории</b>: {items[3]}\n<b>⏳ Время приготовления</b>: {items[4]}"
            await message.answer(message_structure, reply_markup=add_to_favorites(table_name=table_name, pk=items[0]))
            time.sleep(0.5)
        if len(queryset) == 15:
            await bot.send_message(message.chat.id, "Хотите вывести еще?", reply_markup=send_more_recipies_keyboard(
                table_name=table_name
            ))
    except Exception:
        await bot.send_message(message.chat.id, "К сожалению, рецепты закончились(")


@dp.callback_query_handler(add_to_favorites_cd_walk.filter(),
                           lambda call: call['message']['reply_markup']
                                        ['inline_keyboard'][0][0]['text'] == "Добавить в избранные ❤️")
async def add_recipe_to_favorites(callback_query: types.CallbackQuery, callback_data: dict) -> None:
    """
    Function to add recipe to favorites by its pk
        :params
        callback_query - callback from inline keyboard
        callback_data - special data to insert args in callback function
    :return
        None
    """
    try:
        table_name = callback_data.get("table_name")
        pk = callback_data.get("pk")
        add_recipe_to_favorites_table_db(callback_query.message, table_name, pk)
        await bot.send_message(callback_query.message.chat.id, "Вы успешно добавили товар в избранные ✅")
    except IndexError:
        await bot.send_message(callback_query.message.chat.id, "Что-то пошло не так, попробуйте заново  🔄❗")


@logger.catch()
@dp.message_handler(commands=["breakfast"])
async def breakfast(message: types.Message) -> None:
    """
    Function for sending recipies for breakfast
    :param message: Object of message class
    :return: None
    """
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {breakfast.__name__}")
    await send_more_recipies(message=message, table_name='breakfast')


@logger.catch()
@dp.message_handler(commands=["dinner"])
async def dinner(message: types.Message) -> None:
    """
    Function for sending recipies for dinner
    :param message: Object of message class
    :return: None
    """
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {dinner.__name__}")
    await send_more_recipies(message=message, table_name='dinner')


@logger.catch()
@dp.message_handler(commands=["lunch"])
async def lunch(message: types.Message) -> None:
    """
    Function for sending recipies for lunch
    :param message: Object of message class
    :return: None
    """
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {lunch.__name__}")
    await send_more_recipies(message=message, table_name='lunch')


@logger.catch()
@dp.message_handler(commands=["desserts"])
async def desserts(message: types.Message) -> None:
    """
    Function for sending recipies for desserts
    :param
        message: Object of message class
    :return:
        None
    """
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {desserts.__name__}")
    await send_more_recipies(message=message, table_name='desserts')


@logger.catch()
@dp.message_handler(commands=['favorites'])
async def favorites(message: types.Message) -> None:
    """
    Function which send all favorite recipies
    :param
        message: Object of message class
    :return:
        None
    """
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {favorites.__name__}")
    await send_more_recipies(message=message, table_name='favorites')


@dp.callback_query_handler(send_more_recipies_cd_walk.filter())
async def get_answer(callback_query: types.CallbackQuery, callback_data: dict) -> None:
    """
    Callback function to get the answer about sending more recipies from user
    :params
        callback_query - callback from inline keyboard
        callback_data - special data to insert args in callback function
    :return
        None
    """
    global counter_for_breakfast, counter_for_lunch, counter_for_dinner, counter_for_desserts

    if callback_data.get('answer') == 'Да':
        table_name = callback_data.get('table_name')

        if table_name == 'breakfast':
            counter_for_breakfast += 1
            counter = counter_for_breakfast
        elif table_name == 'lunch':
            counter_for_lunch += 1
            counter = counter_for_lunch
        elif table_name == 'dinner':
            counter_for_dinner += 1
            counter = counter_for_dinner
        else:
            counter_for_desserts += 1
            counter = counter_for_desserts
        await send_more_recipies(callback_query.message, quantity_range=counter, table_name=table_name)
    else:
        await bot.send_message(callback_query.message.chat.id, "Я рад, что Вы нашли то, что искали в "
                                                               "наших рецептах 😊")


@logger.catch()
@dp.message_handler(commands=["create"])
async def create_recipe(message: types.Message) -> None:
    """
    Funtion for creating recipies
    :params
        message - object of Message class
    :return
        None
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
    await StatesForCreate.callback_type.set()
    logger.info(f"Пользователь {message.from_user.full_name} перешел в команду {set_title.__name__}")
    try:
        if pattern.search(message.text) is not None:

            async with state.proxy() as data:
                data["title"] = message.text

            await message.answer("✅ Название принято, идем дальше. Из какого рациона дня блюдо?",
                                 reply_markup=type_meal_keyboard())
        else:
            await message.answer("Название должно содержать только буквы! ❌\n"
                                 "Попробуйте еще раз (выберите команду <b>заново</b>)! 🔄❗")
            raise ValueError
    except ValueError:
        await state.reset_state()
        await StatesForCreate.title.set()


@logger.catch()
@dp.callback_query_handler(state=StatesForCreate.callback_type)
async def get_type_callback(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """"""
    await StatesForCreate.time.set()
    logger.info(f"Пользователь {callback_query.message.from_user.full_name} перешел в команду "
                f"{get_type_callback.__name__}")
    try:
        async with state.proxy() as data:
            data["type"] = callback_query.data
            await callback_query.message.answer("✅ Есть, идем дальше. Сколько времени требуется для приготовления "
                                                "блюда?\n<b>(Пример: 3 д 2 ч 1 мин)</b>")
    except Exception:
        await bot.send_message(callback_query.message.chat.id, "Что-то пошло не так в ходе выбора.\n"
                                                               "Давайте попробуем заново 🔄❗")
        await state.reset_state()
        await StatesForCreate.callback_type.set()


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

    try:
        if message.text.replace(" ", "").isalnum():

            async with state.proxy() as data:
                data["time"] = message.text

            await message.answer("✅ Время зафиксировано. Сколько калорий весит блюдо?\n"
                                 "<b>(Пример: 123 ккал)</b>")
        else:
            await message.answer("Количество затраченного времени должно содержать только цифры и буквы! ❌\n"
                                 "Воспользуйтесь примером и попробуйте еще раз (выберите команду <b>заново</b>)! 🔄❗")
            raise ValueError
    except ValueError:
        await state.reset_state()
        await StatesForCreate.time.set()


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

    try:
        if message.text.replace(" ", "").isalnum():

            async with state.proxy() as data:
                data["calories"] = message.text

            await message.answer("Эх, постоянная борьба с калориями... 😔\n"
                                 "⏭ Опишите вкратце этапы приготовления. \n"
                                 "Пример: (1. Разбить яйцо. 2. Добавить муку ...)")
        else:
            await message.answer("Количество калорий должно содержать только буквы и цифры. ❌\n "
                                 "Воспользуйтесь примером и попробуйте еще раз (выберите команду <b>заново</b>)! 🔄❗")
            raise ValueError
    except ValueError:
        await state.reset_state()
        await StatesForCreate.calories.set()


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
        try:
            data["description"] = message.text
            await message.answer("✅ Принято, последний шаг!\n"
                                 "Пришлите фотографию для лучшего отображения 🖼")
        except Exception:
            await bot.send_message(message.chat.id, "Что-то пошло не так в ходе добавления описания.\nУбедитесь, "
                                                    "что Ваш текст соответствует примеру и повторите попытку ❗")
            await state.reset_state()
            await StatesForCreate.description.set()


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
        try:
            photo_url = os.path.abspath(
                os.path.join('images', f"{data['title']}_{message.from_user.id}.png"))
            await message.photo[-1].download(destination_file=photo_url)
            send_data_from_recipe_to_database(message=message, title=data['title'], type_meal=data['type'],
                                              calories=data['calories'],
                                              time=data['time'], description=data['description'], photo=photo_url)
            photo_lsd = open(photo_url, 'rb')
            await bot.send_photo(message.chat.id, photo=photo_lsd, caption=f"Название: {data['title']}😱\n"
                                                                           f"<b>🍽 Блюдо на</b>: {data['type']}\n"
                                                                           f"<b>🍔 Калории</b>: {data['calories']}\n"
                                                                           f"<b>⏳ Время приготовления</b>: "
                                                                           f"{data['time']}\n"
                                                                           f"<b>📖 Описание</b>: {data['description']}")
        except Exception:
            await bot.send_message(message.chat.id, "Что-то пошло не так в ходе обработке фотографии. \n"
                                                    "Попробуйте заново, если ошибка вылезет повторно, то попробуйте"
                                                    "выбрать другую фотографию ❗️")
            await state.reset_state()
            await StatesForCreate.image.set()

        await state.reset_state()


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
                                         f"<b>📖 Описание</b>: {indexes[4]}")


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
