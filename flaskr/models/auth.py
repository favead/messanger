from flask import session
from flaskr.models.user import *
from flaskr.models.error import FlaskrError


def register_user(request_form: dict):  
  username = request_form['username']
  password = request_form['password']
  email = request_form['email']
  user_ = User.create_user(username=username, password=password, email=email)
  if user_ is None:
    raise FlaskrError("Username is already taken")
  else:
    user_ = user_.__data__
  auth_user(user_)


def login_user(request_form: dict):
  username = request_form['username']
  password = request_form['password']
  user_ = User.get_user(username=username)
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

def user_is_logged_in():
  return session['logged_in']

def get_user_id():
  return session['user_id']