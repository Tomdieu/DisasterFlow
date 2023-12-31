import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.http import HttpRequest

from .models import User

class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request:HttpRequest):

        token = request.headers.get('Authorization')

        if not token:

            return None
        
        user_info_url = settings.ACCOUNT_SERVICE+"/api/accounts/user/user-info"
        headers = {'Authorization':token}

        try:

            response = requests.get(user_info_url,headers=headers)
            response.raise_for_status()
            user_data = response.json()
        except requests.RequestException as e:
            raise AuthenticationFailed('Failed to authenticate. Error: {}'.format(str(e)))
        
        # Get the user base on the user_id
        user = User.objects.get(id=user_data['id'])

        return (user, None)