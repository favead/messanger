from peewee import *
from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for, session
from flaskr.models import base
from flaskr.models import user

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET','POST'))
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    error = None

    if username is None:
      error = "Username is required"
    if password is None:
      error = "Password is required"
    if email is None:
      error = "Email is required"
    if error is None:
      with base.database.atomic():
        try:
          user_ = user.UserModel.create(
            username = username,
            password = password,
            email = email
          )
          auth_user(user)
          return redirect(url_for('index'))
        except IntegrityError:
          flash('That username/email is already taken')
    else:
      flash(error)

  return render_template('auth/register.html')


@bp.route('/login', methods=('GET','POST'))
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    error = None

    if username is None:
      error = "Username is required"
    if password is None:
      error = "Password is required"

    if error is None:
      with base.database.atomic():
        try:
          user_ = user.UserModel.get(
            user.UserModel.username == username,
            user.UserModel.password == password
          )
        except user.UserModel.DoesNotExist:
          flash('The password is incorrect or accout doesnt exist')
        else:
          auth_user(user_)
          return redirect(url_for("index"))

  return render_template('auth/login.html')

@bp.route('/logout',methods=['POST'])
def logout():
  if request.method == 'POST':
    logout_user()


def logout_user():
  session['logged_in'] = False
  session['user_id'] = None
  session['username'] = None
  session['email'] = None

def auth_user(user):
  session['logged_in'] = True
  session['user_id'] = user.id
  session['username'] = user.username
  session['email'] = user.email
  flash('You are logged in as %s' % (user.username))