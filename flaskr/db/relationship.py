from flaskr.db.base import Base
from flaskr.db.user import User
from peewee import *

class Relationship(Base):
  from_user = ForeignKeyField(User)
  to_user = ForeignKeyField(User)

  indexes = (
    (('from','to'),True),
  )