
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alerts.models import Alert
else:
    Alert = None

from mapbox import Geocoder

from django.conf import settings

geocoder = Geocoder()

MAPBOX_ACCESS_TOKEN = settings.MAPBOX_ACCESS_TOKEN

def forward_geocode(location):
    response = geocoder.forward(location)
    return response.json()

def reverse_geocode(lat, lng):
    response = geocoder.reverse(lon=lng, lat=lat)
    return response.json()

def extract_location_data(location_data):
    features = location_data['features']
    if len(features) == 0:
        return None
    feature = features[0]
    return {
        'lat': feature['center'][1],
        'lng': feature['center'][0],
        'zip_code': feature['context'][0]['text'],
        'locality': feature['context'][1]['text'],
    }

def get_alerts_within_location(place:str):
    location_data = forward_geocode(place)
    location = extract_location_data(location_data)
    if location is None:
        return []
    alerts = Alert.objects.filter(location__locality=location['locality'])
    return alerts