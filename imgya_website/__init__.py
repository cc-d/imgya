from flask import Flask, session, g, render_template, current_app
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy

def create_app(db=False):
	app = Flask(__name__)
	app.config.from_object('dev_config')
	if db:
		db = SQLAlchemy(app)
		return (app, db)
	return app

(app, db) = create_app(db=True)

with app.app_context():
	from .db import *
	from .auth import *
	from .pages import *
	from .upload import *

app.register_blueprint(auth.bp)
app.register_blueprint(pages.bp)
app.register_blueprint(upload.bp)

from .functions import *