from flask import session
from flaskr.db.user import User
from flaskr.models.error import FlaskrError


def get_current_user():
  if session.get('logged_in'):
    return User.get_user(session['username'])
  else:
    return None

def get_user_by_id(user_id: int):
  user = User.get_by_id(user_id)
  return user
