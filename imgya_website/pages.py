import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, Flask, abort

from .db import *
from .functions import *

bp = Blueprint('pages', __name__)

@bp.route('/')
def index():
	return render_template('base.html')

@bp.route('/i/<image_name>')
def image_page(image_name):
	if not valid_name(image_name, ignore=['.']):
		abort(404)

	if image_name.find('.') == -1:
		db = get_db()
		extension = db.engine.execute("select extension from files where id=%s", base58_decode(image_name))
		extension = extension.fetchone()
		if extension != None:
			extension = extension[0]
			return render_template('image.html', image_name=image_name, image_extension=extension)
		else:
			abort(404)

	else:
		return redirect(current_app.config['FLASK_UPLOAD_SYMLINK'] + image_name)

@bp.route('/a/<album>')
def album_page(album):
	if not valid_name(album):
		abort(404)
	db = get_db()
	ids = db.engine.execute("select file_ids from albums where id=%s", base58_decode(album))
	ids = ids.fetchone()
	if ids != None:
		ids = ids[0].split()
		return render_template('album.html', album_ids=ids)

@bp.route('/d/<file>')
def direct_file(file):
	return redirect(current_app.config['FLASK_UPLOAD_SYMLINK'] + file)