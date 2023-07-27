import json
import os
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
    files_list = ["result_lyogkii-ujin.json", "result_pp-deserty.json", "result_pp-obed.json", "result_pp-zavtrak.json"]
    directory = "/home/alexandr/PycharmProjects/parser_bot_healthy_food/telebot/database/results/"
    for file_name in files_list:
        with open(f"{directory}{file_name}", 'r', encoding='utf-8') as file:
            list_of_dicts = json.loads(file.read())
            for elements in list_of_dicts:
                if file_name == "result_lyogkii-ujin.json":
                    dish_type = "Ужин"
                elif file_name == "result_pp-deserty.json":
                    dish_type = "Десерты"
                elif file_name == "result_pp-obed.json":
                    dish_type = "Обед"
                else:
                    dish_type = "Завтрак"
                with db.atomic():
                    Recipies.get_or_create(
                        title=elements["name"],
                        url=elements["link"],
                        type=dish_type,
                        calories=elements["calories"],
                        time=elements["cooking_time"]
                    )


print(data_for_db())