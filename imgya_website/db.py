from flask import Flask, current_app, g
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint
from imgya_website import create_app

def get_db():
	#app = Flask(__name__)
	#app = Flask(current_app.name)
	#app.config.from_object(current_app.config['CONFIG_NAME'])
	#db = SQLAlchemy(app)
	(app, db) = create_app(db=True)
	return db

def raw_sql(sql):
	db = get_db()
	query_results = db.engine.execute(sql)
	return query_results