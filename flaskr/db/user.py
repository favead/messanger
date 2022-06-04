from peewee import *
from . import base


class UserModel(base.BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField(unique=True)

