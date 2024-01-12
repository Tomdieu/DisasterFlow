from alerts.models import User,Profile,Location
from django.contrib.gis.geos import Point

from . import Event

class UserEvent(Event):

    def update_user(self,data):

        pass

    def create_user(self,data):

        profile = data.pop("profile", None)

        # check if the user does not exists

        user_id = data.get('id')

        exists = User.objects.filter(id=user_id).exists()

        user = None

        if not exists:

            location: dict | None = data.pop('location', None)

            profile: dict | None = data.pop('profile', None)

            user = User.objects.create(**data)


            if profile:
                profile.pop('location', None)
                Profile.objects.create(user=user)

            if location and profile:
                lat = location.pop('lat')
                lng = location.pop('lng')

                point = Point(lng, lat)

                location = Location.objects.create(point=point, **location)
                user.profile.location = location
                user.profile.save()
                user.save()

        return user