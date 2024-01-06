from kafka import KafkaProducer
from json import dumps
import logging

from django.conf import settings

logging.basicConfig(level=logging.INFO)

def publish(method:str,value: dict):
    producer = None
    try:
        producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=lambda x: dumps(x).encode("utf-8"),
        )

        data:dict = {
            'type':method,
            'data':value
        }

        topic = "alerts"

        producer.send(topic,key=method,value=data)

        producer.flush()
    except Exception as e:
        print(f"An Error Occurred: {e}")
        logging.error(" [-] Error in Publishing : %s", e)
    finally:
        if producer is not None:
            producer.close()