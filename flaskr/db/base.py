from peewee import *
from flaskr.config import cfg




database = SqliteDatabase(cfg['DATABASE'], autoconnect=False)


class Base():
  class Meta:
    database = database
