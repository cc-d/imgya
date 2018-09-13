from flask import Flask, current_app, g
from flask_sqlalchemy import SQLAlchemy

def get_db():
	app = Flask(__name__)
	app.config.from_object('dev_config')
	db = SQLAlchemy(app)
	return db

def raw_sql(sql):
	app = Flask(__name__)
	app.config.from_object('dev_config')
	db = SQLAlchemy(app)
	query_results = db.engine.execute(sql)
	return query_results