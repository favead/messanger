from peewee import *
from flask import Blueprint, redirect, render_template, url_for, session, request, flash, jsonify
from flaskr.models import friend, user, base


bp = Blueprint('profile', __name__, url_prefix='/profile')


def get_current_user():
  if session.get('logged_in'):
    return user.UserModel.get(user.UserModel.id == session['user_id'])


@bp.route('/', methods=('GET','POST'))
def profile():
  user = get_current_user()
  return render_template("profile/index.html", user_=user)


@bp.route('/get_all_friends', methods=['POST'])
def get_all_friends():
  user = get_current_user()
  with base.database.atomic():
    try:
      friends = friend.FriendModel.select().where(friend.FriendModel.sec_friend == user)
    except friend.FriendModel.DoesNotExist:
      pass
    else:
      pass


@bp.route('/accept_friend_request', methods=['POST'])
def accept_friend():
  request_data = request.get_json()
  username = request_data['username']    
  from_user = get_current_user()
  with base.database.atomic():
    try:
      to_user = user.UserModel.get(user.UserModel.username == username)
      friend.FriendModel.update(status = 1).where((friend.FriendModel.fir_friend == to_user) &
       (friend.FriendModel.sec_friend == from_user))
    except IntegrityError:
      return jsonify("Something go wrong")
    else:
      return jsonify('Request is accepted')


@bp.route('/send_friend_request', methods=['POST'])
def add_friend():
  request_data = request.get_json()
  username = request_data['username']
  from_user = get_current_user()  
  with base.database.atomic():
    try:
      to_user = user.UserModel.get(user.UserModel.username == username)
      if from_user == to_user:
        return jsonify("Its you :)")
      else:
        friend.FriendModel.create(fir_friend=from_user, sec_friend=to_user, status=0)
    except IntegrityError:
      return jsonify("Request already is send")
    else:
      return jsonify('Request is submit')


@bp.route('/requests', methods=['POST'])
def requests():
  with base.database.atomic():
    try:
      current_user = get_current_user()
      requests = friend.FriendModel.select().where((friend.FriendModel.sec_friend == current_user))
    except friend.FriendModel.DoesNotExist:
      return jsonify({'data':'null'})
    else:
      users = [request.fir_friend.__data__ for request in requests]
      return jsonify({'data':users})


@bp.route('/search', methods=['POST'])
def search():
  request_data = request.get_json()
  start_name = request_data['search']
  with base.database.atomic():
    try:
      users = user.UserModel.select().where(user.UserModel.username.contains(start_name))
    except user.UserModel.DoesNotExist:
      return jsonify('null')
    else:
      response = []
      for user_ in users:
        response.append(user_.__data__)
      return jsonify({'data': response})


