from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from alerts.utils import determine_severity
from . import events

from .models import UserReport,Alert,Event
from api.serializers import AlertListSerializer,UserReportListSerializer
from utils.event_store import create_event_store

from .producer import fanout_publish

@receiver(post_save, sender=UserReport, dispatch_uid="process_report")
def process_report(sender,instance,created,**kwargs):

    if created:

        @transaction.on_commit
        def async_task(instance:UserReport):
            """
            Async Task To Create Alert From User Report
            - Here we are going to create an alert from the user report
            - We are going to use the same location as the user report
            - We are going to use the same title as the user report
            - We are going to use the same description as the user report
            - We are going to use the same type as the user report
            - We are going to use the same severity as the user report
            - From the impact and the urgency we will calculate the severity
            """

            impact = instance.impact
            urgency = instance.urgency

            severity = determine_severity(impact,urgency)

            Alert.objects.create(
                title=instance.title,
                description=instance.description,
                type=instance.type,
                severity=severity,
                location=instance.location,
                created_by=instance.user,
                audience="public"
            )


        async_task(instance)

        create_event_store(events.REPORT_CREATED,UserReportListSerializer(instance).data)
    
    else:
        fanout_publish(events.REPORT_UPDATED,UserReportListSerializer(instance).data)
        pass

@receiver(post_save, sender=Alert, dispatch_uid="process_alert")
def process_alert(sender,instance,created,**kwargs):

    if created:
        create_event_store(events.ALERT_CREATED,AlertListSerializer(instance).data)
        fanout_publish(events.ALERT_CREATED,AlertListSerializer(instance).data)
    else:
        create_event_store(events.ALERT_UPDATED,AlertListSerializer(instance).data)
        fanout_publish(events.ALERT_UPDATED,AlertListSerializer(instance).data)
