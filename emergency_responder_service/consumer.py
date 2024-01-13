
import pika
import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emergency_responder_service.settings")
django.setup()

from core.models import Alert,EmergencyResponder,Location,Profile,AlertLocation

from core import events
from core.utils import Feature

from django.conf import settings

from typing import Any

# Set the timeout to 3 hours (in seconds)
timeout_seconds = 3 * 60 * 60

credentials = pika.PlainCredentials(settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD)
parameters = pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, settings.RABBITMQ_VHOST, credentials,socket_timeout=timeout_seconds)
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

def handle_event(event_type:str,data:dict, method: Any, channel: Any):

    if event_type == events.EMERGENCY_RESPONDER_CREATED:

        profile = data.pop("profile",None)
        data.pop("location",None)

        if not EmergencyResponder.objects.filter(id=data.get('id')).exists():
            user = EmergencyResponder.objects.create(**data)

            if profile:

                profile.pop("user",None)

                profile = Profile.objects.create(user=user,**profile)

            channel.basic_ack(delivery_tag=method.delivery_tag)
            print(" [+] Emergency Responder Created : ",user)
        else:
            channel.basic_ack(delivery_tag=method.delivery_tag)
            print("Emergency Responder Already Exists")
    
    if event_type == events.EMERGENCY_RESPONDER_UPDATED:

        if EmergencyResponder.objects.filter(id=data.get('id')).exists():
        
            user = EmergencyResponder.objects.get(id=data.get("id"))

            profile = data.pop("profile",None)

            for key,value in data.items():
                setattr(user,key,value)

            user.save()

            if profile:

                profile.pop("location",None)
                profile.pop("location",None)

                profile = Profile.objects.get(user=user)

                for key,value in profile.items():
                    setattr(profile,key,value)

                profile.save()
                
                channel.basic_ack(delivery_tag=method.delivery_tag)
                
                print("Emergency Responder {} Updated Successfully".format(user))
        else:
            
                channel.basic_ack(delivery_tag=method.delivery_tag)
            
    if event_type == events.USER_LOCATION_CREATED:
        
        if(EmergencyResponder.objects.filter(id=data.get("user")).exists()):
            user = EmergencyResponder.objects.get(id=data.get("user"))

            lat = data.pop("lat",0)
            lng = data.pop("lng",0)
            data.pop('user',None)
            

            point = "POINT({} {})".format(lng,lat)

            location = Location.objects.create(user=user,point=point,**data)

            user.save()
            
            channel.basic_ack(delivery_tag=method.delivery_tag)

            print(" [+] Location Created For Emergency Responder : ",location)
        else:
            channel.basic_ack(delivery_tag=method.delivery_tag)
            print(" [+] The location created is not for an emergency responder")

    if event_type == events.USER_LOCATION_UPDATED:

        if(EmergencyResponder.objects.filter(id=data.get("user")).exists()):
            user = EmergencyResponder.objects.get(id=data.get("user"))

            lat = data.pop("lat",0)
            lng = data.pop("lng",0)

            point = "POINT({} {})".format(lng,lat)
            
            data.pop('user',None)

            location = Location.objects.get(user=user)

            for key,value in data.items():
                setattr(location,key,value)

            if lat != 0 and lng != 0:
                location.point = point

            location.save()
            
            channel.basic_ack(delivery_tag=method.delivery_tag)

            print(" [+] Location Updated For Emergency Responder : ",location)
            channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            channel.basic_ack(delivery_tag=method.delivery_tag)
            print(" [+] The location updated is not for an emergency responder")

    if event_type == events.ALERT_CREATED:
        
        def extract(location:dict):

            return Feature(**location)

        _location = data.pop("location",None)
        # feature_location = Feature(**_location)
        created_by:dict = data.pop("created_by",None)
        report = data.pop("report",None)

        location = None
        

        if _location:

            location =  extract(_location)

            [lng,lat]= location.geometry.get("coordinates")

            properties = location.properties

            point = "SRID=4326;POINT({} {})".format(lng,lat)

            location = AlertLocation.objects.create(point=point,**properties)
            
        created_by_user_id = created_by.get('id')
        
        image = report.get("image",None)

        Alert.objects.create(image=image,location=location,created_by=created_by_user_id,**data)
        
        channel.basic_ack(delivery_tag=method.delivery_tag)
        
        print("Alert Created Sucessfully ")
    
    elif event_type == events.ALERT_UPDATED:

        location:dict = data.pop("location",None)
        created_by:dict = data.pop("created_by",None)

def callback(ch,method,properties,body):

    content_type = properties.content_type

    delivery_mode = properties.delivery_mode

    message = json.loads(body.decode("utf-8"))

    event_type:str = message.get("type")
    data:dict = message.get("data")

    print("Event : ",event_type)

    print("Data : ",json.dumps(data,indent=4))

    handle_event(event_type,data,method,ch)
        
# Setup consumer for emergency responder queue
    
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)


print(" [*] Waiting for messages. To exit press CTRL+C")

channel.start_consuming()