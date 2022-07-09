from peewee import *
from flaskr.db.relationship import Relationship


cfg = {'DATABASE':'C:/Users/Маша/Desktop/flask/instance/48g.db',
      'SECRET_KEY':'dev',
      'DEBUG':True}

database = SqliteDatabase(cfg['DATABASE'], autoconnect=True)

class Base(Model):
  class Meta:
    database = database



if __name__ == '__main__':
  test_rel()