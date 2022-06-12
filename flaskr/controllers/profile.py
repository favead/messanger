from flask import Blueprint, render_template, request, jsonify
from flaskr.models.friends import create_friend_request, get_friends_for_user
from flaskr.models.friends import get_current_user, update_friend_request, get_friend_requests
from flaskr.models.friends import find_user_by_name
from flaskr.models.error import FlaskrError

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/', methods=('GET','POST'))
def profile():
  user = get_current_user()
  return render_template("profile/index.html", user_=user)


@bp.route('/friends', methods=['POST'])
def get_friends():
  user = get_current_user()
  try:
    friends = get_friends_for_user(user)
  except FlaskrError as e:
    return jsonify(e)
  else:
    return jsonify({'data':friends})


@bp.route('/requests/update', methods=['POST'])
def accept_friend():
  request_data = request.get_json()
  username = request_data['username']    
  to_user = get_current_user()
  try:
    n_r = update_friend_request(1, to_user, username)
  except FlaskrError as e:
    return jsonify(e)
  else:
    print(n_r)
    return jsonify('Request is accepted')


@bp.route('/requests/create', methods=['POST'])
def add_friend():
  request_data = request.get_json()
  username = request_data['username']
  from_user = get_current_user()  
  try:
    create_friend_request(from_user, username)
  except FlaskrError as e:
    return jsonify(e)
  else:
    return jsonify("Request is sent")


@bp.route('/requests', methods=['POST'])
def requests():
  user = get_current_user()
  try:
    requests = get_friend_requests(user)
  except FlaskrError as e:
    return jsonify({'data':'null'})
  else:
    return jsonify({'data':requests})


@bp.route('/search', methods=['POST'])
def search():
  request_data = request.get_json()
  start_name = request_data['search']
  try:
    users = find_user_by_name(start_name)
    print(users)
  except FlaskrError:
    return jsonify({'data':'null'})
  else:
    return jsonify({'data': users})


@bp.route('/test', methods=('GET','POST'))
def test():
  user = get_current_user()
  try:
    friends = get_friends_for_user(user)
  except FlaskrError as e:
    return jsonify(e)
  else:
    return jsonify({'data':friends})