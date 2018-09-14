import os
from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
from werkzeug.utils import secure_filename
from .functions import *
from .db import *

bp = Blueprint('upload', __name__)

def allowed_file(filename):
	if filename.split('.')[-1] not in current_app.config['ALLOWED_EXTENSIONS']:
		return False
	else:
		return True

def reserve_id(filename, extension):
	extension = extension.lower()
	file_type = 'misc'
	for key, value in current_app.config['TYPE_EXTENSIONS'].items():
		if extension in value:
			file_type = key
	db = get_db()
	file_id = db.engine.execute("INSERT INTO files (extension, original_name, type) values (%s, %s, %s); SELECT currval('files_id_seq');",
	(extension, filename, file_type)).fetchone()
	#file_id = db.engine.execute("LASTVAL()").fetchone()
	file_id = base58_encode(file_id[0])
	return file_id

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		
		file = request.files['file']
		
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			extension = filename.split('.')[-1]
			extension = extension.lower()
			file_id = reserve_id(filename, extension)
			base58_filename = file_id + '.' + extension
			file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], base58_filename))
			return redirect(current_app.config['FLASK_UPLOAD_SYMLINK'] + base58_filename)

	return render_template('upload.html')


@bp.route('/images/<filename>')
def uploaded_file(filename):
	return 'test'
