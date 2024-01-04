from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from alerts.models import Alert,Location,UserReport,User,Profile

class LocationSerializer(GeoFeatureModelSerializer):
    
    class Meta:
        model = Location
        geo_field = "point"
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = '__all__'

class UserReportCreateSerializer(serializers.ModelSerializer):
    location = LocationSerializer(write_only=True)
    class Meta:
        model = UserReport
        # fields = '__all__'
        exclude = ['user']

class UserReportListSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    user = UserSerializer()
    class Meta:
        model = UserReport
        fields = '__all__'

class AlertCreateSerializer(serializers.ModelSerializer):
    location = LocationSerializer(write_only=True)
    class Meta:

        model = Alert
        fields = '__all__'

class AlertListSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    created_by = UserSerializer()
    location = LocationSerializer()
    class Meta:

        model = Alert
        fields = '__all__'