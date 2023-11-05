import json
import sqlite3
from aiogram.types import Message
from loguru import logger

con = sqlite3.connect("../database.db")
cursor = con.cursor()


class User:
    """
    Model User is done to keep info about users

    Attrs:
        name - Username
        user _id - user id
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT NOT NULL,
        user_id TEXT NOT NULL
        )
    """)
    con.commit()


class Recipies:
    """
    Model Recipies is done to keep info about recipes, calories and time-wasting for cooking

    Attrs:
        title - dish name
        type - part of day meal (breakfast, lunch, dinner, desserts)
        calories - calories quantity
        time - time spending on cooking
        url - url to site with recipe
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS breakfast (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        calories TEXT NOT NULL,
        time TEXT NOT NULL,
        url TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lunch (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        calories TEXT NOT NULL,
        time TEXT NOT NULL,
        url TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dinner (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        calories TEXT NOT NULL,
        time TEXT NOT NULL,
        url TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS desserts (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        calories TEXT NOT NULL,
        time TEXT NOT NULL,
        url TEXT NOT NULL
        )
    """)
    con.commit()


class Favorites:
    """
    Model to add favorite recipies

    Attrs:
        title - dish name
        type - part of day meal (breakfast, lunch, dinner, desserts)
        calories - calories quantity
        time - time spending on cooking
        url - url to site with recipe
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        calories INTEGER NOT NULL,
        time INTEGER NOT NULL,
        url TEXT,
        user INTEGER,
        FOREIGN KEY (user) REFERENCES user
        )
    """)
    con.commit()


class Create:
    """
    Model to create recipies

    Attrs:
        title - dish name
        calories - calories quantity
        time - time spending on cooking
        type - part of day meal (breakfast, lunch, dinner, desserts)
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS created(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        calories TEXT NOT NULL,
        time TEXT NOT NULL,
        description TEXT NOT NULL,
        photo TEXT NOT NULL,
        user INTEGER,
        FOREIGN KEY (user) REFERENCES user
        )
    """)
    con.commit()


breakfast_list = list()
dinner_list = list()
lunch_list = list()
desserts_list = list()


def data_for_db() -> None:
    """
    Function which open files and collect info about recipies and send it in a dict
    :return - none
    """
    files_list = ["result_lyogkii-ujin.json", "result_pp-deserty.json", "result_pp-obed.json", "result_pp-zavtrak.json"]
    for file_name in files_list:
        with open(f"results/{file_name}", 'r', encoding='windows-1251') as file:
            list_of_dicts = json.loads(file.read())
            for elements in list_of_dicts:
                if file_name == "result_lyogkii-ujin.json":
                    dish_type = "Ужин"
                    structured_info = (elements["id"], elements["name"], dish_type, elements["calories"],
                                       elements["cooking_time"], elements["link"])
                    dinner_list.append(structured_info)
                elif file_name == "result_pp-deserty.json":
                    dish_type = "Десерты"
                    structured_info = (elements["id"], elements["name"], dish_type, elements["calories"],
                                       elements["cooking_time"], elements["link"])
                    desserts_list.append(structured_info)
                elif file_name == "result_pp-obed.json":
                    dish_type = "Обед"
                    structured_info = (elements["id"], elements["name"], dish_type, elements["calories"],
                                       elements["cooking_time"], elements["link"])
                    lunch_list.append(structured_info)
                else:
                    dish_type = "Завтрак"
                    structured_info = (elements["id"], elements["name"], dish_type, elements["calories"],
                                       elements["cooking_time"], elements["link"])
                    breakfast_list.append(structured_info)

    cursor.executemany("INSERT INTO breakfast VALUES (?, ?, ?, ?, ?, ?);", breakfast_list)
    cursor.executemany("INSERT INTO lunch VALUES (?, ?, ?, ?, ?, ?);", lunch_list)
    cursor.executemany("INSERT INTO dinner VALUES (?, ?, ?, ?, ?, ?);", dinner_list)
    cursor.executemany("INSERT INTO desserts VALUES (?, ?, ?, ?, ?, ?);", desserts_list)
    con.commit()


@logger.catch()
def get_data_from_breakfast_table(message: Message, number: int) -> list:
    """
    Function which collect data from breakfast table
    :params
        message - object of Message type
        number - quantity of data to collect
    :return
        list - queryset
    """
    logger.info(f"Пользователь {message.from_user.full_name} "
                f"перешел в функцию {get_data_from_breakfast_table.__name__}")
    cursor.execute("SELECT * FROM breakfast")
    queryset = cursor.fetchmany(number)
    return queryset


@logger.catch()
def get_data_from_lunch_table(message: Message, number: int) -> list:
    """
    Function which collect data from lunch table
    :params
        message - object of Message type
        number - quantity of data to collect
    :return
        list - queryset
    """
    logger.info(f"Пользователь {message.from_user.full_name} "
                f"перешел в функцию {get_data_from_lunch_table.__name__}")
    cursor.execute("SELECT * FROM lunch")
    queryset = cursor.fetchmany(number)
    return queryset


@logger.catch()
def get_data_from_dinner_table(message: Message, number: int) -> list:
    """
    Function which collect data from breakfast table
    :params
        message - object of Message type
        number - quantity of data to collect
    :return
        list - queryset
    """
    logger.info(f"Пользователь {message.from_user.full_name} "
                f"перешел в функцию {get_data_from_dinner_table.__name__}")
    cursor.execute("SELECT * FROM dinner")
    queryset = cursor.fetchmany(number)
    return queryset


@logger.catch()
def get_data_from_desserts_table(message: Message, number: int) -> list:
    """
    Function which collect data from desserts table
    :params
        message - object of Message type
        number - quantity of data to collect
    :return
        list - queryset
    """
    logger.info(f"Пользователь {message.from_user.full_name} "
                f"перешел в функцию {get_data_from_dinner_table.__name__}")
    cursor.execute("SELECT * FROM desserts")
    queryset = cursor.fetchmany(number)
    return queryset


@logger.catch()
def create_user(message: Message):
    """
    Function to create a new user
    :params
        message - object of Message type
    :return
        none
    """
    logger.info(f"Пользователь {message.from_user.full_name} "
                f"перешел в функцию {create_user.__name__}")
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    info = cursor.execute('SELECT * FROM user WHERE user_id=?', (user_id,)).fetchone()
    if info is None:
        cursor.execute("INSERT INTO user VALUES(name, user_id)", (user_name, user_id))
        con.commit()


@logger.catch()
def send_data_from_recipe_to_database(message: Message, title: str, type_meal: str, calories: str, time: str,
                                      photo: list, description: str) -> None:
    """
    Function to create a recipe
    :params
        message - object of Message type
    :return
        none
    """
    logger.info(f"Пользователь {message.from_user.full_name} "
                f"перешел в функцию {send_data_from_recipe_to_database.__name__}")
    user_id = cursor.execute('SELECT * FROM user WHERE user_id=?', (message.from_user.id,)).fetchone()
    primary_user_key = user_id['id']
    print(primary_user_key)
    cursor.execute("INSERT INTO created VALUES (?, ?, ?, ?, ?, ?, ?, ?)", ())
    # con.commit()
