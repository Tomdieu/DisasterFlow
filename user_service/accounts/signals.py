from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import User, Citizen, EmergencyResponder, Location, Profile, Event
from .producer import fanout_publish
from accounts.api.serializers import UserSerializer, ProfileSerializer, LocationSerializer
from . import events
import json


@receiver(post_save, sender=User)
def create_token_and_notify_other_services(sender, instance, created, **kwargs):
    data = json.dumps(UserSerializer(instance).data)
    if created:
        Token.objects.create(user=instance)
        Location.objects.create(user=instance)
        fanout_publish(events.USER_CREATED, data, exchange_name="accounts")
    else:
        fanout_publish(events.USER_UPDATED, data, exchange_name="accounts")


@receiver(post_save, sender=Citizen)
def notify_other_services(sender, instance, created, **kwargs):
    data = json.dumps(UserSerializer(instance).data)
    if created:
        fanout_publish(events.CITIZEN_CREATED, data, exchange_name="accounts")
    else:
        fanout_publish(events.CITIZEN_UPDATED, data, exchange_name="accounts")


@receiver(post_save, sender=EmergencyResponder)
def notify_other_services(sender, instance, created, **kwargs):
    data = json.dumps(UserSerializer(instance).data)
    if created:
        fanout_publish(events.EMERGENCY_RESPONDER_CREATED, data, exchange_name="accounts")
    else:
        fanout_publish(events.EMERGENCY_RESPONDER_UPDATED, data, exchange_name="accounts")


@receiver(post_save, sender=Location)
def create_location_and_notify_other_services(sender, instance, created, **kwargs):
    data = json.dumps(LocationSerializer(instance).data)

    if created:
        fanout_publish(events.USER_LOCATION_CREATED, data, exchange_name="accounts")
    else:
        fanout_publish(events.USER_LOCATION_UPDATED, data, exchange_name="accounts")


@receiver(post_save, sender=Profile)
def create_profile_and_notify_other_services(sender, instance, created, **kwargs):
    data = json.dumps(ProfileSerializer(instance).data)

    if created:
        fanout_publish(events.PROFILE_CREATED, data, exchange_name="accounts")
    else:
        fanout_publish(events.PROFILE_UPDATED, data, exchange_name="accounts")


@receiver(post_delete, sender=User)
def delete_token_and_notify_other_services(sender, instance, **kwargs):

    data = json.dumps(UserSerializer(instance).data)
    fanout_publish(events.USER_DELETED, data, exchange_name="accounts")
