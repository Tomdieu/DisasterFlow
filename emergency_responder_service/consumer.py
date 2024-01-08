
import pika
import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emergency_responder_service.settings")
django.setup()

from core.models import Alert,EmergencyResponder,Location,Profile

from core import events
from core.utils import Feature

from django.conf import settings

credentials = pika.PlainCredentials(settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD)
parameters = pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, settings.RABBITMQ_VHOST, credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

queue_name = "emergency_responder_queue"

channel.queue_declare(queue=queue_name,durable=True)

# Declare a fanout exchange

topic_exchanges = ["accounts","alerts"]

routing_keys = ["accounts.*","alerts.*"]

for exchange in topic_exchanges:

    channel.exchange_declare(exchange=exchange,exchange_type="topic",durable=True)

# Bind queue to the fanout exchange

for exchange,routing_key in list(zip(topic_exchanges,routing_keys)):
    print(" [+] Binding queue to exchange : ",exchange, " with routing key : ",routing_key)
    channel.queue_bind(exchange=exchange, queue=queue_name,routing_key=routing_key)

def handle_event(event_type:str,data:dict):

    if event_type == events.EMERGENCY_RESPONDER_CREATED:

        profile = data.pop("profile",None)

        user = EmergencyResponder.objects.create(**data)

        if profile:

            profile.pop("location",None)

            profile = Profile.objects.create(user=user,**profile)


        print(" [+] Emergency Responder Created : ",user)
    
    if event_type == events.EMERGENCY_RESPONDER_UPDATED:

        user = EmergencyResponder.objects.get(id=data.get("id"))

        profile = data.pop("profile",None)

        for key,value in data.items():
            setattr(user,key,value)

        user.save()

        if profile:

            profile.pop("location",None)

            profile = Profile.objects.get(user=user)

            for key,value in profile.items():
                setattr(profile,key,value)

            profile.save()
    
    if event_type == events.LOCATION_CREATED:
        if(EmergencyResponder.objects.filter(id=data.get("user")).exists()):
            user = EmergencyResponder.objects.get(id=data.get("user"))

            lat = data.pop("lat",0)
            lng = data.pop("lng",0)

            point = "POINT({} {})".format(lng,lat)

            location = Location.objects.create(user=user,point=point,**data)

            user.save()

            print(" [+] Location Created For Emergency Responder : ",location)
        print(" [+] The location created is not for an emergency responder")

    if event_type == events.LOCATION_UPDATED:

        if(EmergencyResponder.objects.filter(id=data.get("user")).exists()):
            user = EmergencyResponder.objects.get(id=data.get("user"))

            lat = data.pop("lat",0)
            lng = data.pop("lng",0)

            point = "POINT({} {})".format(lng,lat)

            location = Location.objects.get(user=user)

            for key,value in data.items():
                setattr(location,key,value)

            if lat != 0 and lng != 0:
                location.point = point

            location.save()

            print(" [+] Location Updated For Emergency Responder : ",location)
        print(" [+] The location updated is not for an emergency responder")

    if event_type == events.ALERT_CREATED:

        _location = data.get("location",None)
        created_by:dict = data.pop("created_by",None)

        def extract(location:dict):

            return Feature(**location)

        if _location:

            location =  extract(_location)

            [lng,lat]= location.geometry.coordinates

            properties = location.properties

            point = "SRID=4326;POINT({} {})".format(lng,lat)

            location = Location.objects.create(point=point,**location)
        created_by_user_id = created_by.get('id')

        Alert.objects.create(location=location,created_by=created_by_user_id,**data)
    
    elif event_type == events.ALERT_UPDATED:

        location:dict = data.pop("location",None)
        created_by:dict = data.pop("created_by",None)

def callback(ch,method,properties,body):

    content_type = properties.content_type

    delivery_mode = properties.delivery_mode

    message = json.loads(body.decode("utf-8"))

    event_type:str = message.get("type")
    data:dict = message.get("data")

    print("Event : ",event_type," Data : ",data)

    # handle_event(event_type,data)

        
# Setup consumer for emergency responder queue
    
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)


print(" [*] Waiting for messages. To exit press CTRL+C")

channel.start_consuming()