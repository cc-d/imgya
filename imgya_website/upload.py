import os
from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
from werkzeug.utils import secure_filename
from .functions import *
from .db import *

bp = Blueprint('upload', __name__)

def allowed_file(filename):
	if filename.split('.')[-1] not in current_app.config['ALLOWED_EXTENSIONS']:
		return False
	return True

def reserve_id(filename, extension, mimetype):
	extension = extension.lower()
	file_types = ['image', 'video', 'audio']

	if mimetype.split('/')[0] in file_types:
		file_type = mimetype.split('/')[0]
		db = get_db()
		file_id = db.engine.execute("INSERT INTO files (extension, original_name, type) values (%s, %s, %s); SELECT currval('files_id_seq');",
		(extension, filename, file_type)).fetchone()
		file_id = base58_encode(file_id[0])
		return file_id
	return False


def upload_file(file):
	if file and allowed_file(file.filename) and file.filename != '':
		filename = secure_filename(file.filename)
		mimetype = file.content_type
		extension = filename.split('.')[-1]
		extension = extension.lower()
		file_id = reserve_id(filename, extension, mimetype)
		base58_filename = file_id + '.' + extension
		file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], base58_filename))
		return base58_filename
	return False

@bp.route('/upload', methods=['GET', 'POST'])
def upload_files():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		
		file_list = request.files.getlist('file')

		if len(file_list) == 0:
			flash('No files selected.')
			return redirect(request.url)

		elif len(file_list) == 1:
			for file in file_list:
				base58_filename = upload_file(file)
				return redirect(current_app.config['FLASK_UPLOAD_SYMLINK'] + base58_filename)

		elif len(file_list) > 1:
			album_files = []
			for file in file_list:
				fid = upload_file(file)
				if fid:
					album_files.append(fid)
				else:
					flash('Invalid File: %s' % file.filename)

			db = get_db()
			album = db.engine.execute("INSERT INTO albums (file_ids) values (%s); SELECT currval('albums_id_seq');",
			(' '.join(album_files))).fetchone()

			album = base58_encode(album[0])
			return redirect('/a/' + album)

	return render_template('upload.html')