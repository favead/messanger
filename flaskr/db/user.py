from peewee import *
from flaskr.db.base import Base, database


class User(Base):
  username = CharField(unique=True)
  password = CharField()
  email = CharField(unique=True)

  @classmethod
  def create_user(cls, username: str, password: str, email: str):
    try:
      with database.atomic():
        user = User.create(
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
        user = User.get(User.username == username)
    except User.DoesNotExist:
      user = None
    return user

  @classmethod
  def get_user_by_part_of_name(cls, part_of_name: str):
    try:
      with database.atomic():
        users = (User
        .select()
        .where(User.username.contains(part_of_name))
        )
    except User.DoesNotExist:
      users = None
    return users