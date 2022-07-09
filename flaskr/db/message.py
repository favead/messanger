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
  def create_message(cls, from_user: User, to_user: User, content: str):
    try:
      with database.atomic():
        relationship = Relationship.get_relationship(from_user, to_user)
        if relationship is not None:
          message = Message.create(
            user_relationship=relationship,
            content=content
          )
        else:
          message = None
    except IntegrityError:
      message = None
    return message

  @classmethod
  def get_messages(cls, from_user, to_user):
    try:
      with database.atomic():
        relationship = Relationship.get_relationship(from_user, to_user)
        if relationship is not None:
          messages = (Message
            .select()
            .where(
              Message.user_relationship == relationship
            )
            .order_by(Message.created_at.asc())
            )
    except Message.DoesNotExist:
       messages = None
    return messages


  @classmethod
  def update_message(cls, from_user: User, to_user: User, new_content: str, id: int, is_read: bool):
    if new_content:
      new_info = {Message.content: new_content, Message.is_read: is_read}
    else:
      new_info = {Message.is_read: is_read}
    try:
      with database.atomic():
        relationship = Relationship.get_relationship(from_user, to_user)
        if relationship is not None:
          with database.atomic():
            new_message = (Message
            .update(new_info)
            .where(
              Message.id == id
            )
            .execute())
        else:
          new_message = None
    except IntegrityError:
      new_message = None
    return new_message
