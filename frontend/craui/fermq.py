from .rmqrpc import call

def get_user(username):
    response = call('get_user', username=username)
    if response:
        return response[0]
    else:
        return None

def register_user(username, email, password_hash):
    return call('register_user', username=username, email=email, password_hash=password_hash)

def send_email(to, subject, body):
    return call('send_email', to=to, subject=subject, body=body)

def get_alerts(username):
    return call('get_alerts', username=username)

def set_alert(username, numerator, denominator, threshold):
    return call('set_alert', username=username, numerator=numerator, denominator=denominator, threshold=threshold)

def delete_alert(username, numerator, denominator, threshold):
    return call('delete_alert', username=username, numerator=numerator, denominator=denominator, threshold=threshold)

def get_currency_rates(currencies):
    return call('get_currency_rates', symbols=currencies)
