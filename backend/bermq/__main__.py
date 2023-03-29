from .rmqrpc import listen
from .smtp import send_email_smtp

def send_email(message):
    send_email_smtp(message['to'], message['subject'], message['body'])
    return 'DONE'

listen(send_email)