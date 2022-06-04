from peewee import *
from flask import Flask, redirect, render_template, Blueprint, request
from flaskr.models import auth

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET','POST'))
def register():
  if request.method == 'POST':
    auth.register_user(request_form=request.form)
  return render_template('auth/register.html')


@bp.route('/login', methods=('GET','POST'))
def login():
  if request.method == 'POST':
    auth.login_user(request.form)
  return render_template('auth/login.html')

@bp.route('/logout',methods=['POST'])
def logout():
  if request.method == 'POST':
    auth.logout_user()
  return render_template('auth/logout.html')