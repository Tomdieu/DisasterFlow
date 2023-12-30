from mapbox import Geocoder

from django.conf import settings

geocoder = Geocoder()

MAPBOX_ACCESS_TOKEN = settings.MAPBOX_ACCESS_TOKEN