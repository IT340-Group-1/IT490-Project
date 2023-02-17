import pika
import ssl
import mysql.connector
from cradb import init_db

rmq_host = 'b-025467d8-cc53-4255-b821-20d1be1f15c6.mq.us-east-1.amazonaws.com'
rmq_port = 5671
rmq_user = 'db'
rmq_password = 'db_pa55w0rd$'

db_host = 'localhost'
db_user = 'craapp'
db_password = 'password'

context = ssl.create_default_context()
ssl_options = pika.SSLOptions(context, rmq_host)
rmq_credentials = pika.PlainCredentials(username=rmq_user, password=rmq_password)
rmq_connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rmq_host, port=rmq_port,
    credentials=rmq_credentials,
    ssl_options=ssl_options))

channel = rmq_connection.channel()
channel.basic_qos(prefetch_count=1)

cradb = mysql.connector.connect(
    host=db_host, user=db_user, password=db_password)

init_db(cradb)

# get_password_hash
channel.queue_declare(queue='get_password_hash')

def get_password_hash(ch, method, props, body):
    answer = ''
    sql = '''SELECT password_hash FROM users WHERE email = %s'''
    with cradb.cursor() as cursor:
        cursor.execute(sql, [body])
        result = cursor.fetchone()
        if result:
            answer = result[0]
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=answer)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='get_password_hash', on_message_callback=get_password_hash)

# register_email
channel.queue_declare(queue='register_email', durable=True)

def register_email(ch, method, props, body):
    sql = '''INSERT INTO users (email, password_hash) VALUES (%s, %s)'''
    with cradb.cursor() as cursor:
        cursor.execute(sql, body.split())
        cradb.commit()
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='register_email', on_message_callback=register_email)

channel.start_consuming()