import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, Flask

from .db import *
from .functions import *

bp = Blueprint('pages', __name__)

@bp.route('/')
def index():
	return render_template('base.html')

@bp.route('/i/<image_name>')
def image_page(image_name):
	if image_name not in current_app.config['HTML_URLS']:
		db = get_db()
		extension = db.engine.execute("select extension from files where id=%s", base58_decode(image_name))
		extension = extension.fetchone()[0]
		return render_template('image_page.html', image_name=image_name, image_extension=extension)
	else:
		return render_template('%s.html')

@bp.route('/d/<file>')
def direct_file(file):
	return redirect(current_app.config['FLASK_UPLOAD_SYMLINK'] + file)