from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient,NewTopic
from json import dumps
import logging

from django.conf import settings

logging.basicConfig(level=logging.INFO)

def create_topic(topic_name: str):
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=settings.BOOTSRAP_SERVERS,
            client_id='user'
        )

        topics = admin_client.list_topics()
        if topic_name in topics:
            logging.info(" [+] Topic Already Exists : ", topic_name)
            print(" [+] Topic Already Exists : ", topic_name)
            return

        topic_list = [NewTopic(name=topic_name, num_partitions=1, replication_factor=1)]
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        logging.info(" [+] Topic Created : ", topic_name)
        print(" [+] Topic Created : ", topic_name)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"An Error Occurred: {e} In Creating Topic")
        logging.error(" [-] Error in Creating Topic : %s", e)


def publish(method:str,value: dict):
    producer = None
    try:
        producer = KafkaProducer(
        bootstrap_servers=[settings.BOOTSRAP_SERVERS],
        value_serializer=lambda x: dumps(x).encode("utf-8"),
        )

        data:dict = {
            'type':method,
            'data':value
        }

        topic = "alerts"
        create_topic(topic)

        producer.send(topic,key=method,value=data)

        producer.flush()
    except Exception as e:
        print(f"An Error Occurred: {e}")
        logging.error(" [-] Error in Publishing : %s", e)
    finally:
        if producer is not None:
            producer.close()