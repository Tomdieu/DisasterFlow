
from typing import TYPE_CHECKING,List

if TYPE_CHECKING:
    from alerts.models import Alert
else:
    Alert = None

from .geoapify import Geoapify

from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

def get_alerts_within_location(place: str, radius: float = 1.0,user_id:int=None) -> List['Alert']:

    """
    Here , the system should return all the alerts within that location at a radius of 1 km
    """

    geoapify = Geoapify()

    location_data = geoapify.forward_geocode(place)

    first_item = location_data.results[0]

    lat,lng = first_item.lat,first_item.lon

    search_point = Point(lng,lat,srid=4326)

    radius__in_km = 1.0

    alerts_within_radius : List[Alert] = []

    if user_id:
        # alerts_within_radius = Alert.objects.filter(
        #     created_by_id=user_id,
        #     location__point__dwithin=(search_point, radius__in_km)
        # )
        alerts_within_radius = Alert.objects.filter(created_by_id=user_id,location__point__distance_lte=(search_point, Distance(km=radius__in_km)))
    else:
        # alerts_within_radius = Alert.objects.filter(
        #     location__point__dwithin=(search_point, radius__in_km)
        # )
        alerts_within_radius = Alert.objects.filter(location__point__distance_lte=(search_point, Distance(km=radius__in_km)))
    # alerts = Alert.objects.filter(location__lat__gte=lat-0.05,location__lat__lte=lat+0.05,location__lng__gte=lng-0.05,location__lng__lte=lng+0.05)

    return alerts_within_radius