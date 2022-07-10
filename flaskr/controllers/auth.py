from peewee import *
from flask import jsonify, redirect, render_template, Blueprint, request, flash, url_for
from flaskr.models.auth import *
from flaskr.models.error import FlaskrError

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET','POST'))
def register():
  if request.method == 'POST':
    err = _verify_form(request.form)
    if err is not None:
      flash(err)
      return
    try:
      register_user(request.form)
    except FlaskrError as e:
      flash(e)
    else:
      return redirect_to('index')
  return render_template('auth/register.html')


@bp.route('/login', methods=('GET','POST'))
def login():
  if request.method == 'POST':
    err = _verify_form(request.form)
    if err is not None:
      flash(err)
      return
    try:
      login_user(request.form)
    except FlaskrError as e:
      flash(e)
    else:
      return redirect_to('index')
  return render_template('auth/login.html')


@bp.route('/logout',methods=['POST'])
def logout():
  if request.method == 'POST':
    logout_user()
    return redirect_to('index')


@bp.route('/getId', methods=['POST'])
def get_id():
  if user_is_logged_in():
    print(get_user_id())
    return jsonify({'id': get_user_id()})
  else:
    return jsonify({'id':'null'})


def _verify_form(form_data: dict) -> str:
  for field in form_data.keys():
    if (form_data[field] is None) or (len(form_data[field]) < 3):
      return '{} is required'.format(field)
  return None


def redirect_to(path: str, is_success_process=True):
  if is_success_process is True:
    return redirect(url_for(path))
