from flaskr.db.message import Message
from flaskr.models.user import get_current_user, get_user_by_id
from flaskr.db.user import User
from flaskr.models.error import FlaskrError
from flaskr.db.relationship import Relationship

def get_messages(current_user: User, to_user_id: int):
  to_user = get_user_by_id(to_user_id)
  if to_user is None:
    raise FlaskrError("User is not exist")
  messages = Message.get_messages(current_user, to_user)
  if messages is None:
    raise FlaskrError("No messages")
  return [message.__data__ for message in messages]


def create_message(to_user_id, current_user, message_content):
  to_user = get_user_by_id(to_user_id)
  message = Message.create_message(current_user, to_user, message_content)
  if message is None:
    raise FlaskrError("I dont know how its can be")
  del message.__data__['user_relationship']
  return message.__data__