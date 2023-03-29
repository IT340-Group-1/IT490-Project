import requests
from datetime import date, timedelta

from bermq.rmqrpc import call
from bermq.smtp import send_email_smtp

def get_users():
    return call('get_users')

def get_alerts(username):
    return call('get_alerts', username=username)

def update_alert(username, numerator, denominator, threshold, last):
    return call('update_alert',
                username=username, numerator=numerator, denominator=denominator,
                threshold=str(threshold), last=str(last))

def unique_symbols(alerts):
    symbols = []
    for alert in alerts:
        if alert['numerator'] not in symbols:
            symbols.append(alert['numerator'])
        if alert['denominator'] not in symbols:
            symbols.append(alert['denominator'])
    return symbols

def get_rates(symbols, base='BTC'):
    url = f'https://api.exchangerate.host/latest?base={base}&symbols={",".join(symbols)}'
    response = requests.get(url)
    data = response.json()
    current_rates = data['rates']
    previous_day = str(date.fromisoformat(data['date']) - timedelta(days=1))
    url = f'https://api.exchangerate.host/{previous_day}?base={base}&symbols={",".join(symbols)}'
    response = requests.get(url)
    previous_rates = response.json()['rates']
    return current_rates, previous_rates

def alert_email_message(numerator, denominator, threshold, ratio):
    return f'''<html><head></head><body>
    <p>Hi,</p>
    <p>The ratio of {numerator} / {denominator} has crossed your alert threshold of {threshold} to {ratio}.</p>
    <p>Thank you.<p>
    </body><html>'''

def alert_triggered(alert, ratio):
    subject = f"CRA Alert on {alert['numerator']}/{alert['denominator']}"
    message = alert_email_message(alert['numerator'], alert['denominator'], alert['threshold'], ratio)
    send_email_smtp(alert['email'], subject, message)

def process_alerts():
    users = get_users()
    alerts = []
    for user in users:
        alerts.extend(get_alerts(user['username']))
    symbols = unique_symbols(alerts)
    current_rates, previous_rates = get_rates(symbols)
    for alert in alerts:
        ratio = current_rates[alert['denominator']] / current_rates[alert['numerator']]
        if not alert['last']:
            alert['last'] = previous_rates[alert['denominator']] / previous_rates[alert['numerator']]
        if alert['last'] < alert['threshold']:
            if alert['threshold'] <= ratio:
                alert_triggered(alert, ratio)
        else:
            if alert['threshold'] >= ratio:
                alert_triggered(alert, ratio)
        update_alert(alert['username'], alert['numerator'], alert['denominator'], alert['threshold'], ratio)

if __name__ == "__main__":
    process_alerts()
