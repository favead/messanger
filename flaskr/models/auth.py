from flaskr.db import base, user
from flask import session, flash, redirect, url_for
from peewee import *


def _verify_form(form_data: dict) -> str:
  for field in form_data.keys():
    if (form_data[field] is None) or (len(form_data[field]) < 3):
      return '{} is required'.format(field)
  return None


def register_user(request_form: dict):
  error = _verify_form(request_form)
  if error is None:
    username = request_form['username']
    password = request_form['password']
    email = request_form['email']
    redirect_page = 'index'
    base.transaction_template(
      try_block = _create_user(username, password, email, redirect_page),
      except_error = IntegrityError,
      except_block = _catch_exception_create_user,
      else_block = None
    )
  else:
    flash(error)
      

def login_user(request_form: dict):
  error = _verify_form(request_form)
  if error is None:
    username = request_form['username']
    password = request_form['password']
    redirect_page = 'index'
    base.transaction_template(
      try_block = _get_user(username, password),
      except_error = user.UserModel.DoesNotExist,
      except_block = catch_exception_get_user,
      else_block = _success_get_user(redirect_page, _get_user(username, password))
    )
  else:
    flash(error)



def _get_user(username: str, password: str):
  user_ = user.UserModel.get(
    user.UserModel.username == username,
    user.UserModel.password == password
  )
  return user_


def catch_exception_get_user():
  flash('The password is incorrect or accout doesnt exist')


def _success_get_user(redirect_page, user):
  auth_user(user)
  return redirect(url_for(redirect_page))


def _create_user(username: str, password: str, email: str, redirect_url: str):
  user_ = user.UserModel.create(
    username = username,
    password = password,
    email = email
  )
  auth_user(user_)
  return redirect(url_for(redirect_url))


def _catch_exception_create_user():
  flash('That username/email is already taken')


def logout_user():
  session['logged_in'] = False
  session['user_id'] = None
  session['username'] = None
  session['email'] = None

def auth_user(user):
  user_ = user.__data__
  print(user_)
  session['logged_in'] = True
  session['user_id'] = user_['id']
  session['username'] = user_['username']
  session['email'] = user_['email']
  flash('You are logged in as %s' % (user_['username']))