import json,os
import logging
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emergency_responder_service.settings")
django.setup()


from kafka import KafkaConsumer

logging.basicConfig(level=logging.DEBUG)


def consume():
    try:
        consumer = KafkaConsumer(
            bootstrap_servers="localhost:9092",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )
        # Define the topic

        topics = ["users", "alerts"]

        consumer.subscribe(topics=topics)

        

        for message in consumer:
            print(" [+] Message Consumed : ", message.value)
    except KeyboardInterrupt:
        logging.info(" [-] Stopping Consumer")
    finally:
        logging.info(" [-] Closing Consumer")
        consumer.close()


if __name__ == "__main__":
    consume()