from . import base
from . import user
from peewee import *


class MessageModel(base.BaseModel):
    user = ForeignKeyField(user.UserModel, backref='messages')
    content = TextField()
    created_at = DateTimeField()