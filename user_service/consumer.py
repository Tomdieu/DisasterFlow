import logging
import json
import os, django
from _kafka import KafkaConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_service.settings')
django.setup()

logging.basicConfig(level=logging.DEBUG)


def consume():
    try:
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 value_deserializer=lambda v: json.loads(v.decode('utf-8')))
        # Define the topic

        topic = "users"

        consumer.subscribe(topics=[topic])

        for message in consumer:
            print(" [+] Message Consumed : ", message.value)
    except Exception as e:
        logging.error(" [-] Error in Consuming : ", e)
