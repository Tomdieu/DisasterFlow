import json
from typing import Any
import logging
from kafka import KafkaProducer

logging.basicConfig(level=logging.DEBUG)


def publish(type: str, body: Any):
    try:
        producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        # Define the topic

        topic = "users"

        data: dict = {"type": type, "data": body}

        body = json.dumps(data)

        producer.send(topic, value=body)

        producer.flush()

        logging.info(" [+] Message Published : ", body)
    except Exception as e:
        print(f"An Error Occurred: {e}")
        logging.error(" [-] Error in Publishing : ", e)
    finally:
        producer.close()