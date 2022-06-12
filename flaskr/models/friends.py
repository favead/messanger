from flaskr.db.user import UserModel
from flaskr.db.friend import FriendModel
from flaskr.models.error import FlaskrError
from flask import session

def get_current_user():
  if session.get('logged_in'):
    return UserModel.get_user(session['username'])


def get_friends_for_user(current_user):
  friends = FriendModel.get_all_friends(current_user)
  users = []
  if friends is None:
    raise FlaskrError("No any friends")
  for friend in friends:
    if friend.from_user == current_user:
      users.append(friend.to_user.__data__)
    else:
      users.append(friend.from_user.__data__)
  return users


def update_friend_request(status, to_user, username):
  from_user = UserModel.get_user(username)
  if from_user is None:
    raise FlaskrError("User is not exist")
  new_request = FriendModel.update_friend_request(status, from_user, to_user)
  if new_request is None:
    raise FlaskrError("Smth go wrong")
  

def create_friend_request(from_user, username):
  to_user = UserModel.get_user(username)
  if to_user is None:
    raise FlaskrError("User is not exist")
  friend_request = FriendModel.create_friend_request(from_user, to_user)
  if friend_request is None:
    raise FlaskrError("Request is already sent")


def get_friend_requests(current_user):
  friend_requests = FriendModel.get_all_requests(current_user)
  if friend_requests is None:
    raise FlaskrError("No any requests")
  return [f.from_user.__data__ for f in friend_requests]


def find_user_by_name(part_of_name):
  users = UserModel.get_user_by_part_of_name(part_of_name)
  if users is None:
    raise FlaskrError("No any users")
  return [user.__data__ for user in users]