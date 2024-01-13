import pika, os, json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alert_service.settings")
django.setup()

from django.conf import settings

from typing import Any

from django.contrib.gis.geos import Point

from alerts.models import User, Profile, Location

from alerts.utils.event_store import create_event_store

from alerts import events

# Set the timeout to 3 hours (in seconds)
timeout_seconds = 3 * 60 * 60

credentials = pika.PlainCredentials(settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD)
parameters = pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, settings.RABBITMQ_VHOST,
                                       credentials,socket_timeout=timeout_seconds)
# credentials = pika.PlainCredentials("guest", "guest")
# parameters = pika.ConnectionParameters("localhost", 5672, "/", credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

queue_name = "alert_queue"

channel.queue_declare(queue=queue_name, durable=True)

# Declare a fanout exchange for the user service

topic_exchange_name = "accounts"

channel.exchange_declare(exchange=topic_exchange_name, exchange_type='topic', durable=True)

# Bind queue to the fanout exchange

channel.queue_bind(exchange=topic_exchange_name, queue=queue_name, routing_key="accounts.*")


def handle_event(event_type: str, data: dict, method: Any, channel: Any):

    if event_type == events.CITIZEN_CREATED or event_type == events.USER_CREATED:

        if data.get('type') == 'Citizen':

            profile = data.pop("profile", None)

            # check if the user does not exists

            user_id = data.get('id')

            exists = User.objects.filter(id=user_id).exists()

            if not exists:

                location: dict | None = data.pop('location', None)

                profile: dict | None = data.pop('profile', None)

                user = User.objects.create(**data)

                # create_event_store(event_type=event_type, data=data)

                if profile:
                    profile.pop('location',None)
                    Profile.objects.create(user=user)

                if location and profile:
                    lat = location.pop('lat')
                    lng = location.pop('lng')

                    point = Point(lng, lat)

                    location = Location.objects.create(point=point, **location)
                    user.profile.location = location
                    user.profile.save()
                    user.save()

                create_event_store(event_type, data)

                print(" [+] User Created : ", user)

                channel.basic_ack(delivery_tag=method.delivery_tag)


    elif event_type == events.CITIZEN_UPDATED or event_type == events.USER_UPDATED:

        if data.get('type') == 'Citizen':

            if User.objects.filter(id=data.get("id")).exists():

                user = User.objects.get(id=data.get("id"))

                profile = data.pop("profile", None)

                for key, value in data.items():
                    setattr(user, key, value)

                user.save()

                create_event_store(event_type=event_type, data=data)
                channel.basic_ack(delivery_tag=method.delivery_tag)
                print(" [+] User Updated : ", user)

            else:
                # channel.basic_ack(delivery_tag=method.delivery_tag)
                print(" [+] User Does Not Exist")

    elif event_type == events.CITIZEN_DELETED or event_type == events.USER_DELETED:

        if User.objects.filter(id=data.get("id")).exists():

            user = User.objects.get(id=data.get("id"))

            user.delete()

            create_event_store(event_type=event_type, data=data)

            print(" [+] User Deleted : ", user)
            channel.basic_ack(delivery_tag=method.delivery_tag)

        else:
            # channel.basic_ack(delivery_tag=method.delivery_tag)
            print(" [+] User Does Not Exist")

    elif event_type == events.PROFILE_CREATED:

        if User.objects.filter(id=data.get("user")).exists():

            user = User.objects.get(id=data.get("user"))

            location = data.pop("location", None)
            data.pop('user',None)

            print("User : ", user)
            print("Data : ", data)

            profile = Profile.objects.create(user=user,**data)

            # profile = Profile.objects.create(user_id=user.id, **data)

            create_event_store(event_type=event_type, data=data)
            channel.basic_ack(delivery_tag=method.delivery_tag)

            print(" [+] Profile Created : ", profile)

    elif event_type == events.PROFILE_UPDATED:

        if User.objects.filter(id=data.get("user")).exists():

            user = User.objects.get(id=data.get("user"))
            profile = Profile.objects.get(user=user)

            location = data.pop("location", None)
            data.pop('user',None)

            for key, value in data.items():
                setattr(profile, key, value)

            profile.save()

            create_event_store(event_type=event_type, data=data)

            print(" [+] Profile Updated : ", profile)
            channel.basic_ack(delivery_tag=method.delivery_tag)

        else:
            # channel.basic_ack(delivery_tag=method.delivery_tag)
            print(" [+] User Does Not Exist")

    elif event_type == events.USER_LOCATION_CREATED:

        if User.objects.filter(id=data.get("user")).exists():

            user = User.objects.get(id=data.get("user"))

            lat = data.pop("lat", 0)
            lng = data.pop("lng", 0)

            data.pop("user", None)

            point = Point(lng, lat)

            location = Location.objects.create(point=point, **data)

            profile = Profile.objects.get(user=user)

            profile.location = location

            profile.save()

            create_event_store(event_type=event_type, data=data)
            channel.basic_ack(delivery_tag=method.delivery_tag)

            print(" [+] Location Created : ", location)

        else:
            # channel.basic_ack(delivery_tag=method.delivery_tag)
            print(" [+] User Does Not Exist")

    elif event_type == events.USER_LOCATION_UPDATED:

        if User.objects.filter(id=data.get("user")).exists():

            user = User.objects.get(id=data.get("user"))

            lat = data.pop("lat", 0)
            lng = data.pop("lng", 0)

            data.pop("user", None)

            point = Point(lng, lat)

            location = Location.objects.get(user=user)

            for key, value in data.items():
                setattr(location, key, value)

            if lat != 0 and lng != 0:
                location.point = point

            location.save()

            create_event_store(event_type=event_type, data=data)

            print(" [+] Location Updated : ", location)
            channel.basic_ack(delivery_tag=method.delivery_tag)

        else:
            # channel.basic_ack(delivery_tag=method.delivery_tag)
            print(" [+] User Does Not Exist")


def callback(ch, method, properties, body):
    content_type = properties.content_type
    delivery_mode = properties.delivery_mode

    message = json.loads(body.decode("utf-8"))

    print("Message : ", message)

    event_type: str = message.get("type")
    data: dict = message.get("data")

    # ch.basic_ack(delivery_tag=method.delivery_tag)

    handle_event(event_type=event_type, data=data, method=method, channel=ch)

    print(" [+] New Message Recieve From Alert Queue")


# Setup consumer for `alert`` queue

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)

print("[*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
