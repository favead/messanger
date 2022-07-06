from peewee import *
from flaskr.db.user import User
from flaskr.db.base import Base, database
from flaskr.db.relationship import Relationship

class Friend(Base):
  status = IntegerField(default=0)
  user_relationship = ForeignKeyField(Relationship) 
  # 1 - accepted
  # 0 - sended 

  @classmethod
  def create_friend_request(cls, from_user, to_user):
    try:
      with database.atomic():
        friend_request = Friend.create(
          from_user=from_user,
          to_user=to_user
        )
    except IntegrityError:
      friend_request = None
    return friend_request
  
  @classmethod
  def get_all_requests(cls, user):
    try:
      with database.atomic():
        friend_requests = (Friend
          .select()
          .where(
            (Friend.to_user == user)
            &
            (Friend.status == 0)
          )
        )
    except Friend.DoesNotExist:
      friend_requests = None
    return friend_requests

  @classmethod
  def get_all_friends(cls, user):
    try:
      with database.atomic():
        friends = (Friend
          .select()
          .where(
            (Friend.status == 1)
             &
            (
              (Friend.from_user == user)
               | 
              (Friend.to_user == user)
            )
          )
        )
    except Friend.DoesNotExist:
      friends = None
    return friends

  @classmethod
  def update_friend_request(cls, status: int, from_user, to_user):
    try:
      with database.atomic():
        new_request = (Friend
        .update({Friend.status: status})
        .where(
          (Friend.from_user == from_user)
           &
          (Friend.to_user == to_user)
        )
        .execute())
    except Friend.DoesNotExist:
      new_request = None
    return new_request
