from flaskr.db.user import UserModel
from flaskr.db.friend import FriendModel
from flaskr.db.message import MessageModel
from flaskr.db.base import database

def init_tables():
  database.connect()
  database.create_tables([UserModel, FriendModel, MessageModel])
  database.close()