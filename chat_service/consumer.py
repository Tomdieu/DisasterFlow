import pika,json
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_service.settings")
django.setup()

from django.conf import settings

from core.models import User, Chat, Message


credentials = pika.PlainCredentials("guest", "guest")
parameters = pika.ConnectionParameters("localhost", 5672, "/", credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

queue_name = "chat_queue"

channel.queue_declare(queue=queue_name,durable=True)

topic_exchanges = ['accounts']
routing_keys = ['accounts.*']

for topic in topic_exchanges:
    channel.exchange_declare(exchange=topic, exchange_type='topic',durable=True)

for topic,routing in zip(topic_exchanges,routing_keys):
    channel.queue_bind(exchange=topic, queue=queue_name, routing_key=routing)

def callback(ch, method, properties, body):

    print("Received in chat_service")

channel.basic_consumer(queue=queue_name, on_message_callback=callback, auto_ack=True)

print("Started Consuming")

channel.start_consuming()