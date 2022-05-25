from peewee import *
from flask import Blueprint, redirect, render_template, url_for, session, request, flash
from flaskr.models import friend, user, base
import json

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/', methods=('GET','POST'))
def profile():
  user = get_current_user()
  return render_template("profile/index.html", user_=user)


@bp.route('/send_friend_request', methods=['POST'])
def add_friend():
  request_data = request.get_json()
  username = request_data['username']    
  with base.database.atomic():
    try:
      from_user = get_current_user()
      to_user = user.UserModel.get(user.UserModel.username == username)
      friend.FriendModel.create(fir_friend=from_user, sec_friend=to_user, fir_friend_accept=True,
      sec_friend_accept=False)
    except IntegrityError:
      return json.dumps("request already is send")
    else:
      return json.dumps('request is submit')


@bp.route('/requests', methods=['POST'])
def requests():
  with base.database.atomic():
    try:
      current_user = get_current_user()
      requests = friend.FriendModel.select().where((friend.FriendModel.sec_friend == current_user) &
      (friend.FriendModel.sec_friend_accept == False))
    except friend.FriendModel.DoesNotExist:
      return json.dumps({'data':'null'})
    else:
      users = [request.fir_friend for request in requests]
      return json.dumps({'data':users})


@bp.route('/search', methods=['POST'])
def search():
  request_data = request.get_json()
  start_name = request_data['search']
  with base.database.atomic():
    try:
      users = user.UserModel.select().where(user.UserModel.username.contains(start_name))
    except user.UserModel.DoesNotExist:
      return json.dumps('null')
    else:
      response = []
      for user_ in users:
        response.append(user_.__data__)
      return json.dumps({'data': response})


def get_current_user():
  if session.get('logged_in'):
    return user.UserModel.get(user.UserModel.id == session['user_id'])