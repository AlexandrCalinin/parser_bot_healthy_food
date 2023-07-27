import json
import os
from peewee import *
import sqlite3

con = sqlite3.connect("bot_data.db")
cursor = con.cursor()


class User:
    """
    Model User is done to keep info about users

    Attrs:
        name - Username
        chat_id - chat id
        user _id - user id
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user
        (id INTEGER PRIMARY KEY UNIQUE,
        name TEXT NOT NULL,
        chat_id TEXT NOT NULL,
        user_id TEXT NOT NULL
        )
    """)


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
        id INTEGER PRIMARY KEY UNIQUE,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        calories TEXT NOT NULL,
        time TEXT NOT NULL,
        url TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lunch (
        id INTEGER PRIMARY KEY UNIQUE,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        calories TEXT NOT NULL,
        time TEXT NOT NULL,
        url TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dinner (
        id INTEGER PRIMARY KEY UNIQUE,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        calories TEXT NOT NULL,
        time TEXT NOT NULL,
        url TEXT NOT NULL
        )
    """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS desserts (
            id INTEGER PRIMARY KEY UNIQUE,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            calories TEXT NOT NULL,
            time TEXT NOT NULL,
            url TEXT NOT NULL
            )
        """)


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
        id INTEGER PRIMARY KEY UNIQUE,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        calories INTEGER NOT NULL,
        time INTEGER NOT NULL,
        url TEXT,
        user INTEGER,
        FOREIGN KEY (user) REFERENCES user
        )
    """)


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
    cursor.close()
