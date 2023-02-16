import pika
import smtplib
import json
from .cred import get_credentials

rmq_host = 'localhost'
rmq_port = 5672
rmq_user = 'be'
rmq_password = 'password'

rmq_connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rmq_host, port=rmq_port,
    credentials=pika.PlainCredentials(username=rmq_user, password=rmq_password)))

channel = rmq_connection.channel()
channel.basic_qos(prefetch_count=1)

smtp_user, smtp_password = get_credentials('craappgoogle.txt')

def send_email_smtp(receiver, subject, body):
    message = f"Subject: {subject}\n\n{body}"

    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()
    smtp_server.login(smtp_user, smtp_password)
    smtp_server.sendmail(smtp_user, receiver, message)
    smtp_server.quit()

# send_email
channel.queue_declare(queue='send_email', durable=True)

def send_email(ch, method, props, body):
    message = json.loads(body)
    send_email_smtp(message['to'], message['subject'], message['body'])
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='send_email', on_message_callback=send_email)

channel.start_consuming()
