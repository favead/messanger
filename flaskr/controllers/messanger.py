from flask import Blueprint, render_template
from flaskr.models.friends import get_current_user, get_friends_for_user

bp = Blueprint('messanger', __name__)

bp.route('/', methods=('GET','POST'))
def handle_index():
  return index


def index():
  user = get_current_user()
  if user is not None:
    friends = get_friends_for_user(user)
  else:
    friends = []
  return render_template('index.html', friends=friends)