import pika,os,json
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alert_service.settings")
django.setup()

from django.conf import settings

from django.contrib.gis.geos import Point

from alerts.models import User,Profile,Location

from alerts import events

credentials = pika.PlainCredentials(settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD)
parameters = pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, settings.RABBITMQ_VHOST, credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='alert',durable=True)

# Declare a fanout exchange for the user service

fanout_exchange_name = "accounts"

channel.exchange_declare(exchange=fanout_exchange_name, exchange_type='fanout')

# Bind queue to the fanout exchange

channel.queue_bind(exchange=fanout_exchange_name, queue='alert')

def callback(ch,method,properties,body):

    content_type = properties.content_type
    delivery_mode = properties.delivery_mode

    message = json.loads(body.decode("utf-8"))

    event_type:str = message.get("type")
    data:dict = message.get("data")

    if event_type == events.CITIZEN_CREATED:

        profile = data.pop("profile",None)

        user = User.objects.create(**data)

        print(" [+] User Created : ",user)
    
    elif event_type == events.CITIZEN_UPDATED:

        user = User.objects.get(id=data.get("id"))

        profile = data.pop("profile",None)

        for key,value in data.items():
            setattr(user,key,value)
        
        user.save()

        print(" [+] User Updated : ",user)
    
    elif event_type == events.CITIZEN_DELETED:

        user = User.objects.get(id=data.get("id"))

        user.delete()

        print(" [+] User Deleted : ",user)

    elif event_type == events.PROFILE_CREATED:

        user = User.objects.get(id=data.get("user"))
        profile = Profile.objects.create(user=user,**data)

        location = data.pop("location",None)

        profile = Profile.objects.create(user=user,**data)

        print(" [+] Profile Created : ",profile)
    
    elif event_type == events.PROFILE_UPDATED:

        user = User.objects.get(id=data.get("user"))
        profile = Profile.objects.get(user=user)

        location = data.pop("location",None)

        for key,value in data.items():
            setattr(profile,key,value)
        
        profile.save()

        print(" [+] Profile Updated : ",profile)

    elif event_type == events.LOCATION_CREATED:

        user = User.objects.get(id=data.get("user"))

        lat = data.pop("lat",0)
        lng = data.pop("lng",0)

        data.pop("user",None)

        point = Point(lng,lat)

        location = Location.objects.create(point=point,**data)

        profile = Profile.objects.get(user=user)

        profile.location = location

        profile.save()

        print(" [+] Location Created : ",location)
    
    elif event_type == events.LOCATION_UPDATED:

        user = User.objects.get(id=data.get("user"))

        lat = data.pop("lat",0)
        lng = data.pop("lng",0)

        data.pop("user",None)

        point = Point(lng,lat)

        location = Location.objects.get(user=user)

        for key,value in data.items():
            setattr(location,key,value)
        
        if lat != 0 and lng != 0:
            location.point = point
        
        location.save()

        print(" [+] Location Updated : ",location)





    print("Method : ",method)
    print("Properties : ",properties)
    print("Body : ")

    print(" [+] New Message Recieve From Alert Queue")

def fanout_callback(ch,method,properties,body):

    print("Method : ",method)
    print("Properties : ",properties)
    print("Body : ")

    print(" [+] New Message Recieve From Fanout Exchange")

    data = json.loads(body)

    print(data)

# Setup consumer for `alert`` queue

channel.basic_consume(queue='alert',on_message_callback=callback,auto_ack=True)

# Setup consumer for the fanout exchange

fanout_queue_name = "fanout_alert_queue"
channel.queue_declare(queue=fanout_queue_name,durable=True)
channel.basic_consume(queue=fanout_queue_name,on_message_callback=fanout_callback,auto_ack=True)


print(" [+] Started Consuming")
channel.start_consuming()