from peewee import *
from flaskr.config import cfg




database = SqliteDatabase(cfg['DATABASE'], autoconnect=False)


class BaseModel(Model):
  class Meta:
    database = database
