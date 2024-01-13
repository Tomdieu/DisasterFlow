import pika,json
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_service.settings")
django.setup()

from django.conf import settings

from core.models import User, Chat, Message

from core import events

# Set the timeout to 3 hours (in seconds)
timeout_seconds = 3 * 60 * 60


credentials = pika.PlainCredentials("guest", "guest")
parameters = pika.ConnectionParameters("localhost", 5672, "/", credentials,socket_timeout=timeout_seconds)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

queue_name = "chat_queue"

channel.queue_declare(queue=queue_name,durable=True)

topic_exchanges = ['accounts','alert_notifications']
routing_keys = ['accounts.*','alert_notifications.*']

for topic in topic_exchanges:
    channel.exchange_declare(exchange=topic, exchange_type='topic',durable=True)

for topic,routing in zip(topic_exchanges,routing_keys):
    channel.queue_bind(exchange=topic, queue=queue_name, routing_key=routing)
    

def handle_event(event_type:str,data:dict,method,channel):
    
    
    if event_type  == events.USER_CREATED:
        
        pass
    
    pass

def callback(ch, method, properties, body):

    message = json.loads(body.decode("utf-8"))
    
    event_type: str = message.get("type")
    data: dict = message.get("data")
    
    handle_event(event_type,data,method,ch)
    
    
    
    print("Received in chat_service")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print("Started Consuming")

channel.start_consuming()