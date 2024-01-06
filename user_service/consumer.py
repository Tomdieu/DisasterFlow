import logging
import json

from _kafka import KafkaConsumer

logging.basicConfig(level=logging.DEBUG)

def consume():

    try:
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',value_deserializer=lambda v: json.loads(v.decode('utf-8')))
        # Define the topic

        topic = "users"

        consumer.subscribe(topics=[topic])

        for message in consumer:
            print(" [+] Message Consumed : ",message.value)
    except Exception as e:
        logging.error(" [-] Error in Consuming : ",e)