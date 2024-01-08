import json
from typing import Any
import logging
from kafka import KafkaProducer
from django.conf import settings

logging.basicConfig(level=logging.INFO)


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

        # message = json.dumps(data)

        producer.send(topic, key=event_type.encode('utf-8'), value=data)
        producer.flush()

        logging.info(" [+] Message Published : ", data," Through Kafka")
        print(" [+] Message Published : ", data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"An Error Occurred: {e} In Publishing Through Kafka")
        logging.error(" [-] Error in Publishing : %s", e)
    finally:
        if producer is not None:
            producer.close()
            logging.info(" [+] Producer Closed")
            print(" [+] Producer Closed")
