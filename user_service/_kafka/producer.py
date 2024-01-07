import json
from typing import Any
import logging
from kafka import KafkaProducer
from django.conf import settings

logging.basicConfig(level=logging.DEBUG)


def publish(event_type: str, body: Any):
    producer = None
    try:
        producer = KafkaProducer(
            bootstrap_servers=settings.BOOTSRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        # Define the topic
        topic = "users"

        data: dict = {"type": event_type, "data": body}

        message = json.dumps(data)

        producer.send(topic,key=event_type, value=message)
        producer.flush()

        logging.info(" [+] Message Published : %s", message)
    except Exception as e:
        print(f"An Error Occurred: {e}")
        logging.error(" [-] Error in Publishing : %s", e)
    finally:
        if producer is not None:
            producer.close()