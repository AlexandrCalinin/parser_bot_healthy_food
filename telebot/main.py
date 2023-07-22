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


def main():
    print("Бот вышел в онлайн...")
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
