import requests
from .geoapify_types import GeoapifyResponse,RoutingResponse
from django.conf import settings

ACCOUNT_SERVICE = settings.ACCOUNT_SERVICE


class Geoapify:

    def __init__(self, api_key=None):
        global ACCOUNT_SERVICE
        self.api_key = api_key or ACCOUNT_SERVICE

    def forward_geocode(self, location:str) -> GeoapifyResponse:
        url = 'https://api.geoapify.com/v1/geocode/search'
        params = {
            'text': location,
            'apiKey': self.api_key,
            'limit': 1,
        }
        response = requests.get(url, params=params)
        return GeoapifyResponse(**response.json())
    
    def reverse_geocode(self, lat:float, lng:float) -> GeoapifyResponse:

        url = 'https://api.geoapify.com/v1/geocode/reverse'
        params = {
            'lat': lat,
            'lon': lng,
            'apiKey': self.api_key,
        }
        response = requests.get(url, params=params)
        return GeoapifyResponse(**response.json()
    )

    def get_routes_between_locations(self, origin:str, destination:str) -> RoutingResponse:
        """
        origin: string, lat|lng
        destination: string, lat|lng
        """
        url = 'https://api.geoapify.com/v1/routing'
        params = {
            'waypoints': f'{origin}|{destination}',
            'apiKey': self.api_key,
        }
        response = requests.get(url, params=params)
        return RoutingResponse(**response.json())