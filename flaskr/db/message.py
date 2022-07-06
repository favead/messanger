from flaskr.db.base import Base, database
from flaskr.db.user import User
from flaskr.db.relationship import Relationship
from peewee import *
from datetime import datetime as dt

class Message(Base):
  user_relationship = ForeignKeyField(Relationship)
  is_read = BooleanField(default=False)
  content = TextField()
  created_at = DateTimeField(default=dt.now())


  @classmethod
  def create_message(cls, from_user, to_user, content):
    try:
      with database.atomic():
        message = Message.create(
          from_user=from_user,
          to_user=to_user,
          content=content
        )
    except IntegrityError:
      message = None
    return message

  @classmethod
  def get_messages(cls, from_user, to_user):
    try:
      with database.atomic():
        messages = (Message
        .select()
        .where(
            (
              (Message.from_user == from_user)
              &
              (Message.to_user == to_user)
            )
            |
            (
              (Message.from_user == to_user)
              &
              (Message.to_user == from_user)
            )
        )
        .order_by(Message.created_at.asc())
        )
    except Message.DoesNotExist:
      messages = None
    return messages


  @classmethod
  def update_message(cls, from_user, to_user, new_content, id):
    try:
      with database.atomic():
        new_message = 0
    except IntegrityError:
      new_message = None
    return new_message
