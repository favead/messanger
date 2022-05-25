from peewee import *
from . import base
from . import user


class FriendModel(base.BaseModel):
    fir_friend = ForeignKeyField(user.UserModel)
    sec_friend = ForeignKeyField(user.UserModel)
    fir_friend_accept = BooleanField
    sec_friend_accept = BooleanField

    class Meta:
        indexes = (
            ((('fir_friend','sec_friend'),True),)
        )