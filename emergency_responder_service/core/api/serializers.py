from rest_framework import serializers
from core.models import EmergencyResponder,EmergencyResponseTeam,Location,Profile,Alert,EmergencyAction,Messages,Resource
from rest_framework_gis.serializers import GeoFeatureModelSerializer

# Serializer for Profile model
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

# Serializer for Location model

class LocationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Location
        geo_field = 'point'
        fields = '__all__'

# Serializer for EmergencyResponder model
class EmergencyResponderSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = EmergencyResponder
        fields = '__all__'

# Serializer to create an EmergencyResponderTeam

class CreateEmergencyResponseTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyResponseTeam
        fields = ['team_name','address','point','specialization']

# Serializer for EmergencyResponseTeam model
class EmergencyResponseTeamSerializer(GeoFeatureModelSerializer):
    members = EmergencyResponderSerializer(many=True, read_only=True)

    class Meta:
        model = EmergencyResponseTeam
        geo_field = 'point'
        fields = '__all__'
# Serializer to add an EmergencyResponder to an EmergencyResponseTeam
class AddOrRemoveMemberSerializer(serializers.Serializer):
    
    emergency_responder_id = serializers.IntegerField()

    class Meta:

        fields = ['emergency_responder_id']

    def validate_emergency_responsder_id(self,value):

        if not EmergencyResponder.objects.filter(id=value).exists():
            raise serializers.ValidationError("Emergency Responder with this id does not exist")
        return EmergencyResponder.objects.get(id=value)

# Serializer for Alert model
class AlertSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Alert
        geo_field = 'point'
        fields = '__all__'

# Serializer for EmergencyAction model
class EmergencyActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyAction
        fields = '__all__'

# Serializer for Messages model
class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'

# Serializer for Messages model
class MessagesListSerializer(serializers.ModelSerializer):
    team = EmergencyResponseTeamSerializer(read_only=True)
    sender = EmergencyResponderSerializer(read_only=True)

    class Meta:
        model = Messages
        fields = '__all__'

# Serializer for Resource model
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

# Serializer for Resource model
class ResourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        # fields = '__all__'
        exclude = ['team']

class RemoveResourceSerializer(serializers.Serializer):
    resource_id = serializers.IntegerField()

    class Meta:
        fields = ['resource_id']

    def validate_resource_id(self,value):
        if not Resource.objects.filter(id=value).exists():
            raise serializers.ValidationError("Resource with this id does not exist")
        return Resource.objects.get(id=value)