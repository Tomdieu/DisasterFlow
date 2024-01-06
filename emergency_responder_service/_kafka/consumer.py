import json,os
import logging
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emergency_responder_service.settings")
django.setup()

from core.models import Alert,EmergencyResponder,Location,Profile

from core import events
from core.utils import Feature

from kafka import KafkaConsumer

logging.basicConfig(level=logging.DEBUG)

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


def consume():
    try:
        consumer = KafkaConsumer(
            bootstrap_servers="localhost:9092",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )
        # Define the topic

        topics = ["users", "alerts"]

        consumer.subscribe(topics=topics)


        # for message in consumer:
        #     print(" [+] Message Consumed : ", message.value)

        while True:

            message = consumer.poll(1000)

            if message:

                if message is None:
                    continue

                for topic, messages in message.items():

                    for msg in messages:
                        
                        message_data = msg.value

                        topic:str = msg.topic

                        key:str = msg.key

                        event_type:str = message_data.get("type")
                        data:dict = message_data.get("data")

                        handle_event(event_type=event_type,data=data)

                        print(" [+] Message Consumed : ", msg.value)

            


    except KeyboardInterrupt:
        logging.info(" [-] Stopping Consumer")
    finally:
        logging.info(" [-] Closing Consumer")
        consumer.close()


if __name__ == "__main__":
    consume()