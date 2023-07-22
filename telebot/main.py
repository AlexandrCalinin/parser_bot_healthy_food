from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN


bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message) -> None:
    """
    Start function
    :param message: Object of message class
    :return: None
    """
    await message.answer("Hello")


@dp.message_handler(commands=["breakfast"])
async def breakfast(message: types.Message) -> None:
    """
    Function for sending recipies for breakfast
    :param message: Object of message class
    :return: None
    """
    pass


def main() -> None:
    """
    Function which start bot
    :return: None
    """
    print("Бот вышел в онлайн...")
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
