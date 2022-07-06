from tkinter.tix import REAL
from flaskr.db.user import User
from flaskr.models.error import FlaskrError

class UserModel:
  __instance = None
  __db_model = User

  def __new__(cls, username: str, password: str):
    cls.__handle_instance_creating(username, password)
    if cls.__instance is None:
      cls.__instance = super(UserModel, cls).__new__(cls)
    return cls.__instance

  def __init__(self, username: str, password: str):
    self.username = username
    self.password = password

  @classmethod
  def __verify_user(cls, username: str, password: str) -> None:
    user = cls.__db_model.get_user(username)
    if user is not None:
      user = user.__data__
      cls.__verify_user_password(password, user)
    else:
      raise FlaskrError("Please check input username")

  @classmethod
  def __verify_user_password(cls, password: str, user: dict) -> None:
    real_password = user['password']
    if real_password != password:
      raise FlaskrError("Incorrect password")

  @classmethod
  def __handle_instance_creating(cls, username: str, password: str):
    try:
      cls.__verify_user(username, password)
    except FlaskrError:
      cls.__instance = 