from flaskr.db.message import MessageModel
from flaskr.models.auth import get_current_user
from flaskr.db.user import UserModel
from flaskr.models.error import FlaskrError

def get_messages(current_user, to_user_username):
  to_user = UserModel.get_user(to_user_username)
  if to_user is None:
    raise FlaskrError("User is not exist")
  messages = MessageModel.get_messages(current_user, to_user)
  if messages is None:
    raise FlaskrError("No messages")
  return [message.__data__ for message in messages]


def create_message(to_user_username, current_user, message_content):
  message = MessageModel.create_message(current_user, to_user, message_content)
  if message is None:
    raise FlaskrError("I dont know how its can be")
  return message.__data__