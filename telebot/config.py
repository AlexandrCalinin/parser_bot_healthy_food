import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DEFAULT_COMMANDS = (
    ('/start', "Запустить бота"),
    ('/help', 'Помощь в выборе команды'),
    ('/breakfast', "Рецепты на завтрак"),
    ('/lunch', "Рецепты на обед"),
    ('/dinner', "Рецепты на ужин"),
    ('/desserts', "Рецепты на десерт"),
    ('/create', "Команда для создания собственного рецепта"),
    ('/create_history', "Выводит все созданные рецепты"),
    ('/favorites', 'Выводит все избранные рецепты')
)
