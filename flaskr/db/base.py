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


def transaction_template(try_block, except_error, except_block, else_block):
    with database.atomic():
        try:
            if try_block is not None:
                try_block()
            else:
                pass
        except except_error if except_error is not None else None:
            if except_block is not None:
                except_block()
            else:
                pass
        else:
            if else_block is not None:
                else_block()
            else:
                pass