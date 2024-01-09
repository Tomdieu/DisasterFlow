from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import User, Citizen, EmergencyResponder, Location, Profile, Event
from .producer import fanout_publish
from accounts.api.serializers import UserSerializer, ProfileSerializer, LocationSerializer
from . import events
import json
from _kafka import publish

from celery import shared_task


@shared_task
def publish_message(event_type, data, exchange_name="accounts"):
    try:
        publish(events.USER_CREATED, data)
        fanout_publish(events.USER_CREATED, data, exchange_name="accounts")
    except Exception as e:
        print("An Execption Occured: ", e)

@receiver(post_save, sender=User, dispatch_uid='create-token-profile-location')
def create_token_and_notify_other_services(sender, instance, created, **kwargs):
    data = UserSerializer(instance).data
    if created:
        Token.objects.create(user=instance)
        Location.objects.create(user=instance)
        Profile.objects.create(user=instance)

        # publish(events.USER_CREATED, data)
        # fanout_publish(events.USER_CREATED, data, exchange_name="accounts")
        publish_message.delay(events.USER_CREATED, data)
    else:
        publish_message.delay(events.USER_UPDATED, data)
        # publish(events.USER_UPDATED, data)
        # fanout_publish(events.USER_UPDATED, data, exchange_name="accounts")


@receiver(post_save, sender=Citizen, dispatch_uid='create-citizen')
def notify_other_services(sender, instance, created, **kwargs):
    data = UserSerializer(instance).data
    if created:
        # publish(events.CITIZEN_CREATED, data)
        # fanout_publish(events.CITIZEN_CREATED, data, exchange_name="accounts")
        publish_message.delay(events.CITIZEN_CREATED, data)
    else:
        # publish(events.CITIZEN_UPDATED, data)
        # fanout_publish(events.CITIZEN_UPDATED, data, exchange_name="accounts")
        publish_message.delay(events.CITIZEN_UPDATED, data)


@receiver(post_save, sender=EmergencyResponder, dispatch_uid='create-emergency-responder')
def notify_other_services(sender, instance, created, **kwargs):
    data = UserSerializer(instance).data
    if created:
        # publish(events.EMERGENCY_RESPONDER_CREATED, data)
        # fanout_publish(events.EMERGENCY_RESPONDER_CREATED, data, exchange_name="accounts")
        publish_message.delay(events.EMERGENCY_RESPONDER_CREATED, data)
    else:
        # publish(events.EMERGENCY_RESPONDER_UPDATED, data)
        # fanout_publish(events.EMERGENCY_RESPONDER_UPDATED, data, exchange_name="accounts")
        publish_message.delay(events.EMERGENCY_RESPONDER_UPDATED, data)


@receiver(post_save, sender=Location, dispatch_uid='create-location')
def create_location_and_notify_other_services(sender, instance, created, **kwargs):
    data = LocationSerializer(instance).data

    if created:
        # publish(events.USER_LOCATION_CREATED, data)
        # fanout_publish(events.USER_LOCATION_CREATED, data, exchange_name="accounts")
        publish_message.delay(events.USER_LOCATION_CREATED, data)
    else:
        # publish(events.USER_LOCATION_UPDATED, data)
        # fanout_publish(events.USER_LOCATION_UPDATED, data, exchange_name="accounts")
        publish_message.delay(events.USER_LOCATION_UPDATED, data)


@receiver(post_save, sender=Profile, dispatch_uid='create-profile')
def create_profile_and_notify_other_services(sender, instance, created, **kwargs):
    data = ProfileSerializer(instance).data

    if created:
        # publish(events.PROFILE_CREATED, data)
        # fanout_publish(events.PROFILE_CREATED, data, exchange_name="accounts")
        publish_message.delay(events.PROFILE_CREATED, data)
    else:
        # publish(events.PROFILE_UPDATED, data)
        # fanout_publish(events.PROFILE_UPDATED, data, exchange_name="accounts")
        publish_message.delay(events.PROFILE_UPDATED, data)


@receiver(post_delete, sender=User, dispatch_uid='delete-token')
def delete_token_and_notify_other_services(sender, instance, **kwargs):
    data = UserSerializer(instance).data
    # fanout_publish(events.USER_DELETED, data, exchange_name="accounts")
    # publish(events.USER_DELETED, data)
    publish_message.delay(events.USER_DELETED, data)
