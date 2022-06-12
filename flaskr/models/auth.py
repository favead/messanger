from flaskr.db.base import *
from flaskr.db.user import *
from flaskr.models.error import FlaskrError
from flask import session


def register_user(request_form: dict):  
  username = request_form['username']
  password = request_form['password']
  email = request_form['email']
  user_ = UserModel.create_user(username=username, password=password, email=email)
  if user_ is None:
    raise FlaskrError("Username is already taken")
  else:
    user_ = user_.__data__
  auth_user(user_)


def login_user(request_form: dict):
  username = request_form['username']
  password = request_form['password']
  user_ = UserModel.get_user(username=username)
  if user_ is None:
    raise FlaskrError("User with this username is not exists")
  else:
    user_ = user_.__data__
  if user_['password'] != password:
    raise FlaskrError("Password is incorrect")
  auth_user(user_)


def logout_user():
  session['logged_in'] = False
  session['user_id'] = None
  session['username'] = None
  session['email'] = None


def auth_user(user_):
  session['logged_in'] = True
  session['user_id'] = user_['id']
  session['username'] = user_['username']
  session['email'] = user_['email']


def get_current_user():
  if session.get('logged_in'):
    return UserModel.get_user(session['username'])
  else:
    return None