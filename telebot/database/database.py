import json
import sqlite3

from aiogram.types import Message
from loguru import logger

con = sqlite3.connect("/Users/sasakalinin/PycharmProjects/parser_bot_healthy_food/telebot/database.db")
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
    Function which open files and collect info about recipies and send to database
    :return - none
    """
    print('start loading data ...')
    files_list = ["result_lyogkii-ujin.json", "result_pp-deserty.json", "result_pp-obed.json", "result_pp-zavtrak.json"]
    for file_name in files_list:
        with open(f"results/{file_name}", 'r', encoding='utf-8') as file:
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
    print('end loading data ...')


@logger.catch()
def get_data_from_table_in_range(message: Message, number: int, table_name: str) -> list:
    """
    Function which collect data from chosen table in a required range
    :params
        message - object of Message type
        number - quantity of required data
        table_name - required table in database
    :return
        list - queryset
    """
    logger.info(f"Пользователь {message.from_user.full_name} "
                f"перешел в функцию get_data_from_desserts_table.{table_name}")
    queryset = cursor.execute(f"SELECT * FROM {table_name} WHERE id > (?) and id < (?)",
                              (number, number + 16)).fetchall()
    return queryset


@logger.catch()
def create_user(message: Message) -> None:
    """
    Function to create a new user
    :params
        message - object of Message type
    :return
        None
    """
    logger.info(f"Пользователь {message.from_user.full_name} "
                f"перешел в функцию {create_user.__name__}")
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    info = cursor.execute('SELECT * FROM user WHERE user_id=?', (user_id,)).fetchone()
    if info is None:
        cursor.execute("INSERT INTO user (name, user_id) VALUES(?, ?)", (user_name, user_id))
        con.commit()


@logger.catch()
def send_data_from_recipe_to_database(message: Message, title: str, type_meal: str, calories: str, time: str,
                                      photo: str, description: str) -> None:
    """
    Function to create a recipe
    :params
        message - object of Message type
    :return
        None
    """
    logger.info(f"Пользователь {message.from_user.full_name} "
                f"перешел в функцию {send_data_from_recipe_to_database.__name__}")
    user_id = cursor.execute('SELECT * FROM user WHERE user_id=?', (message.from_user.id,)).fetchone()
    primary_user_key = user_id[1]
    cursor.execute("INSERT INTO created (title, type, calories, time, description, photo, user) VALUES ("
                   "?, ?, ?, ?, ?, ?, ?)", (title, type_meal, calories, time, description, photo,
                                            primary_user_key))
    con.commit()


@logger.catch()
def get_created_history(message: Message) -> list:
    """
    Get queryset of created products by user_id
    :params
        message - object of Message type
    :return
        list - queryset
    """
    logger.info(f"Пользователь {message.from_user.full_name} "
                f"перешел в функцию {get_created_history.__name__}")
    user_id = message.from_user.id
    query = cursor.execute('SELECT * FROM created WHERE user=?', (user_id,)).fetchall()
    return query
