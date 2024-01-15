from typing import Any

import pika
import json

from .models import Event

from django.conf import settings
import  logging

logging.basicConfig(level=logging.INFO)

def publish(method: str, body: Any, routing_keys: list[str]):
    try:
        credentials = pika.PlainCredentials(settings.RABBIT_MQ_USERNAME, settings.RABBIT_MQ_PASSWORD)
        paramters = pika.ConnectionParameters(host=settings.RABBIT_MQ_HOST, port=5672, virtual_host="/",
                                              credentials=credentials)
        connection = pika.BlockingConnection(paramters)
        channel = connection.channel()

        data: dict = {
            "type": method,
            "data": body
        }

        properties = pika.BasicProperties(content_type=method, delivery_mode=2)

        body = json.dumps(data).encode('utf-8')

        for routing_key in routing_keys:
            channel.basic_publish(exchange="amq.topic", routing_key=routing_key, body=body,
                                  properties=properties)
        connection.close()
    except Exception as e:
        print(e)


def topic_publish(method: str, body: Any, exchange_name: str = "accounts"):
    try:

        credentials = pika.PlainCredentials(settings.RABBIT_MQ_USERNAME, settings.RABBIT_MQ_PASSWORD)

        paramters = pika.ConnectionParameters(host=settings.RABBIT_MQ_HOST, port=5672, virtual_host="/",
                                              credentials=credentials)
        connection = pika.BlockingConnection(paramters)
        channel = connection.channel()

        channel.exchange_declare(exchange=exchange_name, exchange_type="topic",durable=True)

        data: dict = {
            "type": method,
            "data": body
        }

        properties = pika.BasicProperties(content_type=method, delivery_mode=2)

        body = json.dumps(data,indent=4).encode('utf-8')
        
        Event.objects.create(event_type=method,data=data)

        channel.basic_publish(exchange=exchange_name, routing_key="accounts.*", body=body,
                              properties=properties)
        print("[x] Sent message to fanout exchange")
        connection.close()

    except Exception as e:
        print("An Error Occur : {}".format(e))
