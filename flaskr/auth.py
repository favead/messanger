from xml.dom import NotFoundErr
from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for, session
from flaskr.db import Database, IntegrityError

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET','POST'))
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    db = Database()
    error = None

    if username is None:
      error = "Username is required"
    if password is None:
      error = "Password is required"
    if email is None:
      error = "Email is required"


    if error is None:
      try:
        with db.database.atomic():
          db.user.create(username=username, password=password, email=email),
      except IntegrityError:
        error = f"User {username} is already registred"
        return redirect(url_for("auth.login"))
      else:
        return redirect(url_for("auth.login"))
    db.close_connection()
    flash(error)
  
  return render_template('auth/register.html')


@bp.route('/login', methods=('GET','POST'))
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    db = Database()
    error = None

    if username is None:
      error = "Username is required"
    if password is None:
      error = "Password is required"

    if error is None:
      with db.database.atomic():
        users = db.user.select().where(db.user.username == username)
        user = [u for u in users]
        error2 = None
        if len(user) == 0:
          error2 = "user is not Registred"
        else:
          user = user[0]
        db.close_connection()
      if error2:
        flash("user is not registred")
        return redirect(url_for("auth.register"))
      else:
        auth_user(user)
        return redirect(url_for("index"))

  return render_template('auth/login.html')

@bp.route('/logout',methods=('GET','POST'))
def logout():
  if request.method == 'POST':
    db = Database()
    user = None
    users = db.user.select().where(session['user_id'] == db.user.id)
    for u in users:
      user = u
    logout_user(user)
    db.close_connection()
    return redirect(url_for("index"))
  return render_template('auth/logout.html')


def logout_user(user):
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