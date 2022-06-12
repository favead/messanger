from flaskr.db.base import BaseModel
from flaskr.db.user import UserModel
from peewee import *
from datetime import datetime as dt

class MessageModel(BaseModel):
  from_user = ForeignKeyField(UserModel)
  to_user = ForeignKeyField(UserModel)
  is_read = BooleanField(default=False)
  content = TextField()
  created_at = DateTimeField(default=dt.now())