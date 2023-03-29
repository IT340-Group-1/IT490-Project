import ssl
import pika
import uuid
import json
from .rmq_url import rmq_url

rmq_host = rmq_url().split('//')[1].split(':')[0]
rmq_port = 5671
rmq_user = 'admin'
rmq_password = 'RMQ-Pa55w0rd'

context = ssl.create_default_context()
ssl_options = pika.SSLOptions(context, rmq_host)
rmq_credentials = pika.PlainCredentials(username=rmq_user, password=rmq_password)

def get_rmq_connection():
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=rmq_host, port=rmq_port,
        credentials=rmq_credentials,
        ssl_options=ssl_options))

class RMQRPCClient:

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

def call(rpc_queue, **kwargs):
   return json.loads(RMQRPCClient(rpc_queue).call(json.dumps(kwargs, default=float)))

class Listener:
    def __init__(self, function):
        self.f = function
    
    def callback(self, ch, method, props, body):
        answer = self.f(json.loads(body))
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=json.dumps(answer, default=float))
        ch.basic_ack(delivery_tag=method.delivery_tag)

def listen(*functions):
    connection = get_rmq_connection()
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    for function in functions:
        rpc_queue = function.__name__
        channel.queue_declare(queue=rpc_queue)
        channel.basic_consume(queue=rpc_queue, on_message_callback=Listener(function).callback)
    channel.start_consuming()
