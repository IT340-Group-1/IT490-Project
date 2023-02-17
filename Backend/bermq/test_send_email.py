import pika
import json

def send_message(email, subject, body):
    rmq_host = 'localhost'
    rmq_port = 5672
    rmq_user = 'be'
    rmq_password = 'password'

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rmq_host, port=rmq_port,
        credentials=pika.PlainCredentials(username=rmq_user, password=rmq_password)))

    channel = connection.channel()
    channel.queue_declare(queue='send_email', durable=True)
    message = json.dumps({"to": email, "subject": subject, "body": body})
    channel.basic_publish(exchange="", routing_key="email_queue", body=message)
    connection.close()

if __name__ == "__main__":
    send_message("cns27@njit.edu", "Test Email", "This is a test email sent from RabbitMQ. pls work")