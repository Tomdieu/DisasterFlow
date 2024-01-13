from alerts.models import Alert,User
from django.contrib.gis.geos import Point
from .types import Feature
from alerts.api.serializers import LocationSerializer,AlertListSerializer
from alerts.producer import publish
from alerts import events


def send_alert_notification_to_user(alert:Alert):
    """
    Here we get all the users that are 500 meters from the alert location
    """
    
    serializer = LocationSerializer(alert.location)
    feature_location = Feature(**serializer.data)
    
    alert_serializer = AlertListSerializer(alert)

    coordinates = feature_location.geometry.get("coordinates")
    
    lat = coordinates[1]
    lng = coordinates[0]
    
    search_point = Point(lng,lat,srid=4326)

    radius_in_meters = 500

    users = User.objects.filter(profile__location__point__distance_lte=(search_point, radius_in_meters))
    
    # users = User.objects.filter(location__point__dwithin=(search_point, radius__in_meters))

    for user in users:
        body = {
            "user": user.id,
            "alert": alert_serializer.data,
            "location": feature_location
        }
        
        publish(events.ALERT_NOTIFICATION_SENT,body,exchange_name="notifications",routing_key="notifications.")
        print(" [+] Alert Notification Sent To User : ",user)