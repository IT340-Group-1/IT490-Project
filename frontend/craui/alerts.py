import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from .auth import login_required
from .fermq import get_alerts, set_alert, delete_alert, get_currency_rates

bp = Blueprint('alerts', __name__)

@bp.route('/')
def index():
    username = session.get('username')
    if username is None:
        return render_template('index.html')
    else:
        currencies = ['USD', 'EUR', 'GBP', 'BTC', 'BAM', 'INR', 'AUD']
        currency_rates = session.get('currencyrates')
        if currency_rates is None:
            currency_rates = get_currency_rates(currencies)['current']
            session['currencyrates'] = currency_rates
        user_alerts = get_alerts(username)
        return render_template('alerts/index.html', currencies=currencies, rates=currency_rates, alerts=user_alerts)

@bp.route('/set', methods=('POST',))
@login_required
def set_a():
    username = session.get('username')
    numerator = request.form['numerator']
    denominator = request.form['denominator']
    threshold = request.form['threshold']
    set_alert(username, numerator, denominator, threshold)
    return redirect(url_for('alerts.index'))

@bp.route('/delete/<numerator>/<denominator>/<threshold>', methods=('POST',))
@login_required
def delete_a(numerator, denominator, threshold):
    username = session.get('username')
    delete_alert(username, numerator, denominator, threshold)
    return redirect(url_for('alerts.index'))