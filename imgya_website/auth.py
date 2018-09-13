import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash

from .db import *

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    db = get_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.engine.execute(
            "SELECT id FROM users WHERE username = %s;", (username)
        ).fetchone() is not None:
            error = 'User %s is already registered.' % (username)

        if error is None:
            db.engine.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s);",
                (username, generate_password_hash(password))
            )
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    db = get_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        user = db.engine.execute(
            "SELECT * FROM users WHERE username = %s;", (username)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect('/')

        flash(error)

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('/'))

@bp.before_app_request
def load_logged_in_user():
    db = get_db()
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.engine.execute(
            "SELECT * FROM users WHERE id = %s;", (user_id)
        ).fetchone()