from select import select
from flask import Blueprint, redirect, render_template, url_for, session, request, flash
from flaskr.db import Database, IntegrityError


bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/', methods=('GET','POST'))
def profile():
  users_temp = None
  if request.method == 'POST':
    search = request.form['search']
    db = Database()

    if search is None:
      return

    with db.database.atomic():
      try:
        users = db.user.select().where(db.user.username == search)
        user = None
        for u in users:
          user = u
        if user is None:
          error = "Not found"
          return render_template("profile/index.html",username=session['username'],
                                email = session['email'], users=None)
      except error:
        pass
      else:
        users_temp = [user]
    
    db.close_connection()
  return render_template("profile/index.html",username=session['username'],
  email = session['email'], users=users_temp)



@bp.route('/add_friend', methods=('POST'))
def add_friend():
  if request.method == 'POST':
    username = request.form['username']
    db = Database()

    with db.database.atomic():
      user_select = db.user.select().where(db.user.username == username)
      user = [u for u in user_select][0]
      db.friends.create(fir_friend=session['user_id'], sec_friend=user.id, fir_friend_accept=True,
      sec_friend_accept=False)

    db.close_connection()
  return redirect(url_for('profile.profile'))
  

@bp.route('/test', methods=('GET','POST'))
def test():
  db = Database()
  with db.database.atomic():
    rel_select = db.friends.select().where((db.friends.fir_friend == session['user_id']) | (db.friends.sec_friend == session['user_id']))
    rel = [r for r in rel_select]
    print(rel)
  db.close_connection()

  return render_template("profile/test.html", rel = rel, user_id = session['user_id'])

