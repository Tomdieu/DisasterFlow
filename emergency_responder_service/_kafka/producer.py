from kafka import KafkaProducer
from json import dumps


def publish(event_type:str,body:dict):

    producer = None

    try:

        producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=lambda x: dumps(x).encode("utf-8"),
        )

        data:dict = {
            'type':event_type,
            'data':body
        }

        topic = "emergency_responder"

        producer.send(topic,key=event_type,value=data)

        producer.flush()

    except Exception as e:
        print(f"An Error Occurred: {e}")
    finally:
        if producer is not None:
            producer.close()