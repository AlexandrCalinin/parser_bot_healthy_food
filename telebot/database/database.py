import json
import os
from pathlib import Path

import requests
from peewee import *

db = SqliteDatabase(os.path.join('database', 'bot_data.db'))


class BaseModel(Model):
    """Base class model for ORM peewee"""

    class Meta:
        database: SqliteDatabase = db


class User(BaseModel):
    """
    Model User is done to keep info about users

    Attrs:
        name - Username
        chat_id - chat id
        user _id - user id
    """
    name = CharField()
    chat_id = IntegerField()
    user_id = IntegerField(unique=True)


class Recipies(BaseModel):
    """
    Model Recipies is done to keep info about recipes, calories and time-wasting for cooking

    Attrs:
        title - dish name
        type - part of day meal (breakfast, lunch, dinner, desserts)
        calories - calories quantity
        time - time spending on cooking
        url - url to site with recipe
        image - url to dish photo
    """
    title = CharField(max_length=100)
    type = CharField()
    calories = IntegerField()
    time = IntegerField()
    image = CharField()
    url = CharField()


class Favorites(BaseModel):
    title = CharField()
    type = CharField()
    calories = IntegerField()
    time = IntegerField()
    image = CharField()
    url = CharField()
    user = ForeignKeyField(User)


def data_for_db() -> dict:
    """
    Function which open files and collect info about recipies and send it in a dict
    :return - dict
    """
    directory = "C:/parser_bot_healthy_food/scripts_for_scraping/results"
    for files in Path(directory).glob("*json"):
        with open(files, 'r', encoding='utf-8') as file:
            file_dict = json.loads(file.read())
            for name, url in file_dict.items():
                pass


print(data_for_db())
