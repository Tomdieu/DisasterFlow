
import pika
import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emergency_responder_service.settings")
django.setup()

from core.models import EmergencyResponseTeam,Alert,EmergencyAction,Messages,Resource,EmergencyResponder,Location,Profile

from core import events

from django.conf import settings

credentials = pika.PlainCredentials(settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD)
parameters = pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, settings.RABBITMQ_VHOST, credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='emergency_responder',durable=True)

# Declare a fanout exchange for the user service

fanout_exchange_name = "accounts"

channel.exchange_declare(exchange=fanout_exchange_name, exchange_type='fanout')

# Bind queue to the fanout exchange

channel.queue_bind(exchange=fanout_exchange_name, queue='emergency_responder')

def callback(ch,method,properties,body):

    content_type = properties.content_type

    delivery_mode = properties.delivery_mode

    message = json.loads(body.decode("utf-8"))

    event_type:str = message.get("type")
    data:dict = message.get("data")

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

# Setup consumer for emergency responder
    
channel.basic_consume(queue='emergency_responder', on_message_callback=callback, auto_ack=True)

# Setup Consumer for fanout exchange

fanout_queue_name = "emergency_responder"
channel.queue_declare(queue=fanout_exchange_name, durable=True)
channel.basic_consume(queue=fanout_queue_name, on_message_callback=callback, auto_ack=True)

print(" [+] Started Consuming")