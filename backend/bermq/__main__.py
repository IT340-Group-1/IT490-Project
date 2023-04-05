from .rmqrpc import listen
from .smtp import send_email_smtp
from .currency_rates import get_rates

def send_email(message):
    send_email_smtp(message['to'], message['subject'], message['body'])
    return 'DONE'

def get_currency_rates(r):
    current_rates, previous_rates = get_rates(r['symbols'])
    return {'current': current_rates, 'previous': previous_rates}

listen(send_email, get_currency_rates)