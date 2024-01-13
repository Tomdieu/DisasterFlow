from asgiref.sync import async_to_sync, sync_to_async
from django.db.models.signals import post_save
from django.dispatch import receiver
from alerts.utils.send_alert_notification_to_user import send_alert_notification_to_user

from alerts.utils import determine_severity
from . import events

from .models import UserReport, Alert, Location
from alerts.api.serializers import AlertListSerializer, UserReportListSerializer, LocationSerializer
from alerts.utils.event_store import create_event_store

from alerts.utils import Geoapify

from .producer import topic_publish


@receiver(post_save, sender=Location, dispatch_uid="process_location")
def process_location(sender, instance: Location, created, **kwargs):
    """We are goin to make a backword geocoding base on the latitude and longitude of the location to geoapify"""

    def fill_location_detail(instance: Location):
        geoapify = Geoapify()
        response = geoapify.reverse_geocode(instance.point.y, instance.point.x)
        instance.address = response.results[0].formatted
        instance.state = response.results[0].state
        instance.country = response.results[0].country
        instance.city = response.results[0].city
        instance.save()

    if created:

        try:

            fill_location_detail(instance)
        except Exception as e:
            print("An Error Occur : {}".format(e))
        finally:
            create_event_store(events.LOCATION_CREATED, LocationSerializer(instance).data)


@receiver(post_save, sender=UserReport, dispatch_uid="process_report")
def process_report(sender, instance, created, **kwargs):
    if created:

        def task(user_report: UserReport):
            """
            Async Task To Create Alert From User Report
            - Here we are going to create an alert from the user report
            - We are going to use the same location as the user report
            - We are going to use the same type as the user report
            - We are going to use the same severity as the user report
            - From the impact and the urgency we will calculate the severity
            """

            impact = user_report.impact
            urgency = user_report.urgency

            severity = determine_severity(impact, urgency)

            print("Location : ",user_report.location)

            Alert.objects.create(
                type=user_report.type,
                severity=severity,
                location=user_report.location,
                created_by=user_report.user,
                audience="public",
                report=user_report
            )

        task(instance)

        create_event_store(
            events.REPORT_CREATED, UserReportListSerializer(instance).data
        )

    else:
        topic_publish(events.REPORT_UPDATED, UserReportListSerializer(instance).data)
        pass


@receiver(post_save, sender=Alert, dispatch_uid="process_alert")
def process_alert(sender, instance, created, **kwargs):
    if created:
        send_alert_notification_to_user(instance)
        create_event_store(events.ALERT_CREATED, AlertListSerializer(instance).data)
        topic_publish(events.ALERT_CREATED, AlertListSerializer(instance).data)
    else:
        create_event_store(events.ALERT_UPDATED, AlertListSerializer(instance).data)
        topic_publish(events.ALERT_UPDATED, AlertListSerializer(instance).data)
