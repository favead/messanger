import os
from . import config
from flask import Flask, render_template, g
from flaskr.db import init_tables
from flaskr.db import base

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




  from flaskr.controllers import auth
  app.register_blueprint(auth.bp)

  from flaskr.controllers import profile
  app.register_blueprint(profile.bp)    

  from flaskr.controllers import messanger
  app.register_blueprint(messanger.bp)
  app.add_url_rule('/', view_func=messanger.index)

  @app.before_request
  def _db_connect():
      base.database.connect()

  @app.teardown_request
  def _db_close(exc):
      if not base.database.is_closed():
          base.database.close()

  init_tables()

  return app