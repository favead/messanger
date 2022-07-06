from flask import Blueprint, render_template
from flaskr.models.friends import get_friends_for_user
from flaskr.models.auth import get_current_user
from flaskr.models.messanger import get_messages, create_message

bp = Blueprint('messanger', __name__)

bp.route('/', methods=('GET','POST'))
def handle_index():
  return index


bp.route('/messages', methods=['POST'])
def get_messages():
  current_user = get_current_user()
  to_user = 


bp.route('/messages/create', methods=['POST'])
def create_message():
  pass


bp.route('/messages/update', methods=['POST'])
def update_message():
  pass


bp.route('/messages/delete', methods=['POST'])
def delete_message():
  pass


def index():
  user = get_current_user()
  if user is not None:
    friends = get_friends_for_user(user)
  else:
    friends = []
  return render_template('index.html', friends=friends)