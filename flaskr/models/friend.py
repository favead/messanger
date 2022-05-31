from peewee import *
from . import base
from . import user


class FriendModel(base.BaseModel):
    fir_friend = ForeignKeyField(user.UserModel)
    sec_friend = ForeignKeyField(user.UserModel)
    status = IntegerField
    # 0 - accepted, -1 - fir send from sec, 1 sec send from fir
    class Meta:
        indexes = (
            ((('fir_friend','sec_friend'),True),)
        )