from peewee import *
from flaskr.config import cfg




database = SqliteDatabase(cfg['DATABASE'], autoconnect=False)


class Base(Model):
  class Meta:
    database = database
