from flaskr.db.user import User
from flaskr.db.friend import Friend
from flaskr.models.error import FlaskrError
from flask import session


def get_friends_for_user(current_user):
  friends = Friend.get_all_friends(current_user)
  users = []
  if friends is None:
    raise FlaskrError("No any friends")
  users = [f.to_user.__data__ if f.from_user == current_user else f.from_user.__data__ for f in friends]
 # for friend in friends:
 #   if friend.from_user == current_user:
 #     users.append(friend.to_user.__data__)
 #   else:
 #     users.append(friend.from_user.__data__)
  return users


def update_friend_request(status, to_user, username):
  from_user = User.get_user(username)
  if from_user is None:
    raise FlaskrError("User is not exist")
  new_request = Friend.update_friend_request(status, from_user, to_user)
  if new_request is None:
    raise FlaskrError("Smth go wrong")
  

def create_friend_request(from_user, username):
  to_user = User.get_user(username)
  if to_user is None:
    raise FlaskrError("User is not exist")
  friend_request = Friend.create_friend_request(from_user, to_user)
  if friend_request is None:
    raise FlaskrError("Request is already sent")


def get_friend_requests(current_user):
  friend_requests = Friend.get_all_requests(current_user)
  if friend_requests is None:
    raise FlaskrError("No any requests")
  return [f.from_user.__data__ for f in friend_requests]


def find_user_by_name(part_of_name):
  users = User.get_user_by_part_of_name(part_of_name)
  if users is None:
    raise FlaskrError("No any users")
  return [user.__data__ for user in users]