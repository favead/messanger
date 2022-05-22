from peewee import *
import click
import os

from sqlalchemy import Boolean

from . import config


database = SqliteDatabase(config.cfg['DATABASE'])


class BaseModel(Model):
    class Meta:
        database = database


class UserModel(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField(unique=True)

    def add_friend():
        pass

class MessageModel(BaseModel):
    user = ForeignKeyField(UserModel, backref='messages')
    content = TextField()
    created_at = DateTimeField()


class FriendModel(BaseModel):
    fir_friend = ForeignKeyField(UserModel)
    sec_friend = ForeignKeyField(UserModel)
    fir_friend_accept = Boolean
    sec_friend_accept = Boolean

    class Meta:
        indexes = (
            ((('fir_friend','sec_friend'),True),)
        )


class RelationshipModel(BaseModel):
    from_user = ForeignKeyField(UserModel, backref='related_from')
    to_user = ForeignKeyField(UserModel, backref='related_to')

    class Meta:
        indexes = (
            ((('from_user','to_user'),True),)
        )


class Database:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance


    def __init__(self):
        self.is_connected = False
        self.database = SqliteDatabase(config.cfg['DATABASE'])
        self.user = UserModel
        self.relationship = RelationshipModel
        self.message = MessageModel
        self.friends = FriendModel


    def open_connection(self):
        print("opened")
        if self.is_connected is False:
            self.database.connect()
            self.is_connected = True


    def close_connection(self):
        print("closed")
        if self.is_connected is True:
            self.database.close()
            self.is_connected = False

    
    def init_tables(self):
        with self.database:
            self.database.create_tables([UserModel, RelationshipModel, FriendModel, MessageModel])
