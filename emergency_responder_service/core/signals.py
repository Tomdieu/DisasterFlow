from django.dispatch import receiver
from django.contrib.gis.geos import Point
from django.db.models.signals import post_save

# from 

from .models import Alert,EmergencyNotification,EmergencyResponseTeam
from core.api.serializers import AlertLocationSerializer
from core.utils import Feature


@receiver(post_save,sender=Alert)
def send_notification_to_all_emergency_responsder_team_located_arround_10km_from_alert_source(sender,instance:Alert,created,**kwargs):
    
    
    if created:
        
        
        alert:Alert = instance
        serializer = AlertLocationSerializer(instance.location)
        feature_location = Feature(**serializer.data)
        
        coordinates = feature_location.geometry.get("coordinates")
        
        lat = coordinates[1]
        lng = coordinates[0]
        
        search_point = Point(lng,lat,srid=4326)
        
        radius_in_km = 10.0
        
        emergency_response_team = EmergencyResponseTeam.objects.filter(point__distance_lte=(search_point,radius_in_km))
        
        for emergency_team in emergency_response_team:
            EmergencyNotification.objects.create(alert=alert,team=emergency_team,message=f"Alert of type : {alert.type} and severity : {alert.severity} Notify at Location : [{lng}:{lat}] if you are capable to handle it please go to rescue")
        

@receiver(post_save,sender=EmergencyNotification)
def send_message_to_alert_reporter(sender,instance,created,**kwargs):
    
    if created:
        
        pass