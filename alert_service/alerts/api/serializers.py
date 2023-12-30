from rest_framework import serializers

from alerts.models import Alert,Location,UserReport,User,Profile

class LocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Location
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

    class Meta:
        model = UserReport
        fields = '__all__'

class UserReportListSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    class Meta:
        model = UserReport
        fields = '__all__'

class AlertCreateSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    class Meta:

        model = Alert
        fields = '__all__'

class AlertListSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    class Meta:

        model = Alert
        fields = '__all__'