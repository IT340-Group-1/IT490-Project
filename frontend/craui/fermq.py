import pika
import ssl
import uuid
import json
from .rmq_url import rmq_url

rmq_host = rmq_url().split('//')[1].split(':')[0]
rmq_port = 5671
rmq_user = 'fe'
rmq_password = 'f3_pa55w0rd$'

context = ssl.create_default_context()
ssl_options = pika.SSLOptions(context, rmq_host)
rmq_credentials = pika.PlainCredentials(username=rmq_user, password=rmq_password)

def get_rmq_connection():
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=rmq_host, port=rmq_port,
        credentials=rmq_credentials,
        ssl_options=ssl_options))

class RMQRPCClient(object):

    def __init__(self, rpc_queue):
        self.rpc_queue = rpc_queue
        self.connection = get_rmq_connection()
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, request):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.rpc_queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=request)
        self.connection.process_data_events(time_limit=None)
        return self.response

def get_password_hash(email):
    return RMQRPCClient('get_password_hash').call(email)

def register_email(email, password_hash):
    connection = get_rmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue='register_email', durable=True)
    message = ' '.join([email, password_hash])
    channel.basic_publish(
        exchange='',
        routing_key='register_email',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    connection.close()

def send_email(to, subject, body):
    connection = get_rmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue='send_email', durable=True)
    message = json.dumps({"to": to, "subject": subject, "body": body})
    channel.basic_publish(
        exchange='',
        routing_key='send_email',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    connection.close()