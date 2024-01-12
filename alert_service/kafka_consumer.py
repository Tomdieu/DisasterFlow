import json, os, django
from json import loads
import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alert_service.settings")
django.setup()

from django.conf import settings
from django.contrib.gis.geos import Point
from alerts.models import User, Profile, Location
from alerts.utils.event_store import create_event_store
from alerts import events

from kafka import KafkaConsumer
from time import sleep

logging.basicConfig(level=logging.INFO)


def process_message(event_type: str, data: dict):
    if event_type == events.CITIZEN_CREATED:
        profile = data.pop("profile", None)

        user = User.objects.create(**data)

        create_event_store(event_type=event_type, data=data)

        print(" [+] User Created : ", user)

    elif event_type == events.CITIZEN_UPDATED:
        if User.objects.filter(id=data.get("id")).exists():
            user = User.objects.get(id=data.get("id"))

            profile = data.pop("profile", None)

            for key, value in data.items():
                setattr(user, key, value)

            user.save()

            create_event_store(event_type=event_type, data=data)

            print(" [+] User Updated : ", user)

        else:
            print(" [+] User Does Not Exist")

    elif event_type == events.CITIZEN_DELETED:
        if User.objects.filter(id=data.get("id")).exists():
            user = User.objects.get(id=data.get("id"))

            user.delete()

            create_event_store(event_type=event_type, data=data)

            print(" [+] User Deleted : ", user)

        else:
            print(" [+] User Does Not Exist")

    elif event_type == events.PROFILE_CREATED:
        if User.objects.filter(id=data.get("id")).exists():
            user = User.objects.get(id=data.get("user"))
            profile = Profile.objects.create(user=user, **data)

            location = data.pop("location", None)

            profile = Profile.objects.create(user=user, **data)

            create_event_store(event_type=event_type, data=data)

            print(" [+] Profile Created : ", profile)

    elif event_type == events.PROFILE_UPDATED:
        if User.objects.filter(id=data.get("id")).exists():
            user = User.objects.get(id=data.get("user"))
            profile = Profile.objects.get(user=user)

            location = data.pop("location", None)

            for key, value in data.items():
                setattr(profile, key, value)

            profile.save()

            create_event_store(event_type=event_type, data=data)

            print(" [+] Profile Updated : ", profile)

        else:
            print(" [+] User Does Not Exist")

    elif event_type == events.USER_LOCATION_CREATED:
        if User.objects.filter(id=data.get("id")).exists():
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

            print(" [+] Location Created : ", location)

        else:
            print(" [+] User Does Not Exist")

    elif event_type == events.USER_LOCATION_UPDATED:
        if User.objects.filter(id=data.get("id")).exists():
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

        else:
            print(" [+] User Does Not Exist")


def consume(topics: list[str]):
    consumer = KafkaConsumer(
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        group_id="alert_group",
        value_deserializer=lambda x: loads(x.decode("utf-8")),
    )

    consumer.subscribe(topics)

    try:
        while True:

            logging.info(" [*] Waiting for messages. To exit press CTRL+C")

            message = consumer.poll(1000)

            if message:

                if message is None:
                    continue

                for topic, messages in message.items():
                    logging.info(f"Processing messages for topic {topic}")

                    # print("Topic : ",topic, " Messages : ",messages)

                    for msg in messages:
                        message_data = msg.value

                        topic: str = msg.topic

                        key: str = msg.key

                        event_type: str = message_data.get("type", None)
                        data: dict = message_data.get("data", None)

                        print("Even Type : ", event_type, " Data : ", data)

                        process_message(event_type=event_type,data=data)

                        print(" [+] Message Consumed : ", msg.value)


    except KeyboardInterrupt:
        logging.info("[-] Stopping Consumer")
        print("\n[!] Keyboard interrupt received. Closing Kafka consumer.")
    finally:
        logging.info("[-] Closing Consumer")
        consumer.close()


if __name__ == "__main__":
    consume(["users"])
