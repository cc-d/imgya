from .db import raw_sql, get_db
from flask import Flask, session, g, render_template
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('dev_config')
db = SQLAlchemy(app)

from .auth import *
from .pages import *

app.register_blueprint(auth.bp)
app.register_blueprint(pages.bp)

from .functions import *