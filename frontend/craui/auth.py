from flask import current_app
import jwt
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import fermq

bp = Blueprint('auth', __name__, url_prefix='/auth')


def verify_email_message(token):
    return f'''<html><head></head><body>
    <p>Hi,</p>
    <p>In order to register your email with Currency Ratio Alerter service,
    please click the link below:<br>
    <a href={url_for('auth.verify_email', token=token, _external=True)}>verify email</a></p>
    <p>Thank you.<p>
    </body><html>'''

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
            if fermq.get_password_hash(email):
                error = f"Email {email} is already registered."
            else:
                token = jwt.encode({"email": email, "password_hash": generate_password_hash(password)},
                                   current_app.config['SECRET_KEY'],
                                   algorithm='HS256')
                fermq.send_email(email, "Welcome to CRA", verify_email_message(token))
                return render_template('auth/verify.html')
        flash(error)

    return render_template('auth/register.html')


@bp.route('/verify-email/<token>')
def verify_email(token):
    data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    email = data['email']
    password_hash = data['password_hash']
    fermq.register_email(email, password_hash)
    flash('Thank you for verifying your email. You should now be able to log in.')
    return redirect(url_for('auth.login'))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = None

        password_hash = fermq.get_password_hash(email).decode()
        if password_hash == '':
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
