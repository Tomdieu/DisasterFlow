# Kafka

## 1. Producer (Users Service)

```py
from confluent_kafka import Producer
import json

# Kafka producer configuration
producer_config = {
    'bootstrap.servers': 'your_kafka_broker',  # Replace with your Kafka broker(s)
}

producer = Producer(producer_config)

# Produce a message to the 'users' topic with event type 'user_created'
topic = 'users'
event_type = 'user_created'
user_data = {'user_id': 123, 'username': 'john_doe'}

message_payload = {
    'event_type': event_type,
    'data': user_data,
}

producer.produce(topic, value=json.dumps(message_payload))

# Close the producer
producer.flush()
```

## 2. Consumer (Alerts, Resource, Communication Services):

```py
from confluent_kafka import Consumer, KafkaError
import json

# Kafka consumer configuration
consumer_config = {
    'bootstrap.servers': 'your_kafka_broker',  # Replace with your Kafka broker(s)
    'group.id': 'alerts_consumer_group',  # Replace with your consumer group
    'auto.offset.reset': 'earliest',
}

consumer = Consumer(consumer_config)

# Subscribe to the 'users' topic
topic = 'users'
consumer.subscribe([topic])

# Start consuming messages
while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break

    # Process the received message
    message_payload = json.loads(msg.value())
    event_type = message_payload.get('event_type')
    data = message_payload.get('data')

    if event_type == 'user_created':
        # Process user_created event
        print(f'Received user_created event. User data: {data}')
    elif event_type == 'user_updated':
        # Process user_updated event
        print(f'Received user_updated event. User data: {data}')
    # Add more conditions for other event types as needed

# Close the consumer
consumer.close()
```

# RabbitMQ

## 1. Producer (Users Service)

```py
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='user_events', exchange_type='fanout')

user_data = {'user_id': 123, 'username': 'john_doe'}  # Replace with actual user data
message_body = json.dumps(user_data)

channel.basic_publish(exchange='user_events', routing_key='', body=message_body)

print(f" [x] Sent {message_body}")

connection.close()

```

## 2. Consumer (Alerts, Resource, Communication Services):

```py
import pika
import json

def callback(ch, method, properties, body):
    user_data = json.loads(body)
    # Process the user data as needed

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='user_events', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='user_events', queue=queue_name)

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
```

