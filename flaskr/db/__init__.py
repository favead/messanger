from flaskr.db.user import User
from flaskr.db.friend import Friend
from flaskr.db.message import Message
from flaskr.db.base import database
from flaskr.db.relationship import Relationship

def init_tables():
  database.connect()
  database.drop_tables([ User, Friend, Message, Relationship ])
  database.create_tables([ User, Friend, Message, Relationship ])
  database.close()