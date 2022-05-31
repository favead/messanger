from peewee import *
import click
import os
from flaskr.config import cfg


database = SqliteDatabase(cfg['DATABASE'])


class BaseModel(Model):
    class Meta:
        database = database


def close_connection():
    database.close()
    print('connection is close.')
