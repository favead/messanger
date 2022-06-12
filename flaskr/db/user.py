from peewee import *
from flaskr.db.base import BaseModel, database


class UserModel(BaseModel):
  username = CharField(unique=True)
  password = CharField()
  email = CharField(unique=True)

  @classmethod
  def create_user(cls, username: str, password: str, email: str):
    try:
      with database.atomic():
        user = UserModel.create(
        username=username,
        password=password,
        email=email
      )
    except IntegrityError:
      user = None
    return user

  @classmethod
  def get_user(cls, username: str):
    try:
      with database.atomic():
        user = UserModel.get(UserModel.username == username)
    except UserModel.DoesNotExist:
      user = None
    return user

  @classmethod
  def get_user_by_part_of_name(cls, part_of_name: str):
    try:
      with database.atomic():
        users = (UserModel
        .select()
        .where(UserModel.username.contains(part_of_name))
        )
    except UserModel.DoesNotExist:
      users = None
    return users