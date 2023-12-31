from confluent_kafka import Producer

p = Producer({
    'bootstrap.servers': 'localhost:9092'
})

def delivery_report(err,msg):

    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def publish(topic:str,event_type:str, data:str):
    global p
    message_payload = {
        'event_type':event_type,
        'data':data
    }

    p.produce(topic, message_payload.encode('utf-8'), callback=delivery_report)
    
# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()