import os
from . import config
from flask import Flask, render_template, g
from flaskr.models import base

def create_app(test_config=None):
  
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(config.cfg)

  if test_config is None:
    app.config.from_pyfile('config.py', silent=True)
  else:
    app.config.from_mapping(test_config)

  try:
      os.makedirs(app.instance_path)
  except OSError:
      pass

  @app.route('/')
  def index():
    return render_template('index.html')

  from flaskr.controllers import auth
  app.register_blueprint(auth.bp)

  from flaskr.controllers import profile
  app.register_blueprint(profile.bp)    


  return app