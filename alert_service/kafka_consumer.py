from confluent_kafka import Consumer
from django.conf import settings

c = Consumer({
    'bootstrap.servers': settings.KAFKA_SERVER,
    'group.id': 'alert_service',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['user'])

while True:

    message = c.poll(1.0)

    if message is None:
        continue

    if message.error():
        print("Consumer error : {}".format(message.error()))

    print("Recieve Message : {}".format(message.value().decode('utf-8')))

c.close()