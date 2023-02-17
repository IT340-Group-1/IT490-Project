import pika
import ssl
import smtplib
import json
from .cred import get_credentials

rmq_host = 'b-025467d8-cc53-4255-b821-20d1be1f15c6.mq.us-east-1.amazonaws.com'
rmq_port = 5671
rmq_user = 'be'
rmq_password = 'b3_pa55w0rd$'

context = ssl.create_default_context()
ssl_options = pika.SSLOptions(context, rmq_host)
rmq_credentials = pika.PlainCredentials(username=rmq_user, password=rmq_password)
rmq_connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rmq_host, port=rmq_port,
    credentials=rmq_credentials,
    ssl_options=ssl_options))

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
