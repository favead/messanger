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
        relationship = Relationship.create_relationship(from_user, to_user)
        friend_request = Friend.create(
          user_relationship=relationship
        )
    except IntegrityError:
      friend_request = None
    return friend_request
  
  @classmethod
  def get_all_requests(cls, user: User):
    friend_requests = []
    try:
      with database.atomic():
        friend_requests = cls.__get_all_template(user, 0)
    except Friend.DoesNotExist:
      friend_requests = None
    return friend_requests

  @classmethod
  def get_all_friends(cls, user: User):
    friends = []
    try:
      with database.atomic():
        friends = cls.__get_all_template(user, 1)
    except Friend.DoesNotExist:
      friends = None
    print(friends)
    return friends

  @classmethod
  def __get_all_template(cls, user: User, status_code: int):
    relationships = []
    users_list = []
    if status_code == 0:
      relationships = Relationship.get_relationships_by_user(user)
    elif status_code == 1:
      relationships = Relationship.get_relationships(user)  

    if relationships is not None:
      for relationship in relationships:
        users = (
          (Friend
          .select()
          .where(
            (Friend.user_relationship == relationship) 
            &
            (Friend.status == status_code)
          ))
        )
        users_list = [u.user_relationship.from_user if u.user_relationship.from_user != user else u.user_relationship.to_user for u in users]
        return users_list
    else:
      return None

  @classmethod
  def update_friend_request(cls, status: int, from_user: User, to_user: User):
    try:
      relationship = Relationship.get_relationship(from_user, to_user)
      if relationship is not None:
        with database.atomic():
          new_request = (Friend
          .update({Friend.status: status})
          .where(
            Friend.user_relationship == relationship
          )
          .execute())
      else:
        new_request = None  
    except Friend.DoesNotExist:
      new_request = None
    return new_request
