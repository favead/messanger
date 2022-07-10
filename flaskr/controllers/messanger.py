from flask import Blueprint, render_template, request, jsonify
from flaskr.models.error import FlaskrError
from flaskr.models.friends import get_friends_for_user
from flaskr.models.user import get_current_user
from flaskr.models.messanger import get_messages, create_message

bp = Blueprint('messanger', __name__)

@bp.route('/', methods=('GET','POST'))
def index():
  user = get_current_user()
  friends = []
  if user is not None:
    try:
      friends = get_friends_for_user(user)
    except:
      pass
  return render_template('index.html', friends=friends)


@bp.route('/messages', methods=['POST'])
def get_all_messages():
  current_user = get_current_user()
  request_data = request.get_json()
  another_user_id = request_data['user_id']
  try:
    messages = get_messages(current_user, another_user_id)
  except FlaskrError as e:
    return jsonify({'data': e})
  else:
    
    return jsonify({'data': messages})


@bp.route('/messages/create', methods=['POST'])
def create_new_message():
  current_user = get_current_user()
  request_data = request.get_json()
  another_user_id = request_data['user_id']
  message_content = request_data['content']
  try:
    message = create_message(another_user_id, current_user, message_content)
  except FlaskrError as e:
    return jsonify({'data': 'null'})
  else:
    return jsonify({'data': message})

@bp.route('/messages/update', methods=['POST'])
def update_message():
  pass


@bp.route('/messages/delete', methods=['POST'])
def delete_message():
  pass


def index():
  user = get_current_user()
  if user is not None:
    friends = get_friends_for_user(user)
  else:
    friends = []
  return render_template('index.html', friends=friends)