import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash

from .db import *
from .functions import *

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    db = get_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        error = None

        if not username or not valid_username(username):
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email or not valid_email(email):
            error = 'Email is required.'
        elif db.engine.execute("SELECT id FROM users WHERE username = %s;", (username)).fetchone() is not None:
            error = 'User %s is already registered.' % (username)

        if error is None:
            reg = db.engine.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s);",
                (username, generate_password_hash(password), email)
            )
            if reg is None:
                error = 'Unable to register new account'
            elif error is None and reg is not None:
                user = db.engine.execute("SELECT * FROM users WHERE username = %s;", (username)).fetchone()
                session.clear()
                session['user_id'] = user['id']

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    db = get_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if valid_email(username):
            email = username
            authtype = 'email'
        else:
            authtype = 'username'

        error = None

        if authtype == 'username' and valid_username(username):
            user = db.engine.execute(
                "SELECT * FROM users WHERE username = %s;", (username)).fetchone()
            if user is None:
                error = 'Incorrect username or email.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'

        elif authtype == 'email' or valid_email(email):
            user = db.engine.execute(
                "SELECT * FROM users WHERE email = %s;", (email)).fetchone()
            if user is None:
                error = 'Incorrect username or email.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'
        else:
            error = 'Invalid username or email.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect('/')

        flash(error)

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@bp.before_app_request
def load_logged_in_user():
    db = get_db()
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.engine.execute("SELECT * FROM users WHERE id = %s;", (user_id)).fetchone()