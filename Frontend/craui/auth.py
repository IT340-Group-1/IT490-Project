import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import rmq

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            if rmq.is_registered(email):
                error = f"Email {email} is already registered."
            else:
                rmq.register_email(email, generate_password_hash(password))
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = None

        password_hash = rmq.get_password_hash(email)
        if password_hash is None:
            error = 'Incorrect email.'
        elif not check_password_hash(password_hash, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_email'] = email
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.before_app_request
def load_logged_in_user():
    user_email = session.get('user_email')

    if user_email is None:
        g.user = None
    else:
        g.user = {'email': user_email}


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_email') is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view