from peewee import *
from flaskr.db.user import UserModel
from flaskr.db.base import BaseModel, database


class FriendModel(BaseModel):
  status = IntegerField(default=0)
  from_user = ForeignKeyField(UserModel)
  to_user = ForeignKeyField(UserModel)   
  # 1 - accepted
  # 0 - sended 

  @classmethod
  def create_friend_request(cls, from_user, to_user):
    try:
      with database.atomic():
        friend_request = FriendModel.create(
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
        friend_requests = (FriendModel
          .select()
          .where(
            (FriendModel.to_user == user)
            &
            (FriendModel.status == 0)
          )
        )
    except FriendModel.DoesNotExist:
      friend_requests = None
    return friend_requests

  @classmethod
  def get_all_friends(cls, user):
    try:
      with database.atomic():
        friends = (FriendModel
          .select()
          .where(
            (FriendModel.status == 1)
             &
            (
              (FriendModel.from_user == user)
               | 
              (FriendModel.to_user == user)
            )
          )
        )
    except FriendModel.DoesNotExist:
      friends = None
    return friends

  @classmethod
  def update_friend_request(cls, status: int, from_user, to_user):
    try:
      with database.atomic():
        new_request = (FriendModel
        .update({FriendModel.status: status})
        .where(
          (FriendModel.from_user == from_user)
           &
          (FriendModel.to_user == to_user)
        )
        .execute())
    except FriendModel.DoesNotExist:
      new_request = None
    return new_request
