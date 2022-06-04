from peewee import *
from . import base
from . import user


class RelationshipModel(base.BaseModel):
    from_user = ForeignKeyField(user.UserModel, backref='related_from')
    to_user = ForeignKeyField(user.UserModel, backref='related_to')

    class Meta:
        indexes = (
            ((('from_user','to_user'),True),)
        )