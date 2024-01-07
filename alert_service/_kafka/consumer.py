from kafka import KafkaConsumer
import json, os, django
from json import loads

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alert_service.settings")
django.setup()


from django.conf import settings
from django.contrib.gis.geos import Point
from alerts.models import User, Profile, Location
from alerts.utils.event_store import create_event_store
from alerts import events


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
        bootstrap_servers=["localhost:9092"],
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        group_id="alert_group",
        value_deserializer=lambda x: loads(x.decode("utf-8")),
    )

    consumer.subscribe(topics)

    for message in consumer:
        if message:
            message_value: dict = message.value
            topic:str = message.topic
            key:str = message.key

            event_type: str = message_value.get("type")
            data: dict = message_value.get("data")

            process_message(event_type=event_type, data=data)
if __name__ == "__main__":
    consume(["users"])
