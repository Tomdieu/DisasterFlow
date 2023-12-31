from rest_framework import serializers
from rest_framework import fields
from accounts.models import Profile, Citizen, EmergencyResponder, EmergencyResponseTeam, User


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=120, help_text="old password")
    new_password = serializers.CharField(max_length=120, help_text="new password")
    confirm_new_password = serializers.CharField(max_length=120, help_text="confirmation of the new password")

    class Meta:
        extra_kwargs = {
            "old_password": {"required": True},
            "new_password": {"required": True},
            "confirm_password": {"required": True},
        }


class LoginSerializer(serializers.Serializer):
    email = fields.CharField(required=True, max_length=120, help_text="User's email")
    password = fields.CharField(
        required=True, max_length=120, help_text="User's password"
    )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['location', 'skills', 'interest', 'is_online', 'last_activity']


class CitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = ['username', 'email', 'type', 'date_of_birth', 'profile_image', 'phone_number', "home_address"]

        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": True,
            },
            "email": {
                "required": True,
            },
        }


class CitizenListSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Citizen
        fields = ['username', 'email', 'type', 'date_of_birth', 'profile_image', 'phone_number', "home_address"]


class EmergencyResponderSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyResponder
        fields = ['username', 'email', 'type', 'date_of_birth', 'profile_image', 'phone_number',
                  "emergency_contact_number", "emergency_contact_person"]

        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": True,
            },
            "email": {
                "required": True,
            },
        }


class EmergencyResponderListSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = EmergencyResponder
        fields = ['username', 'email', 'type', 'date_of_birth', 'profile_image', 'phone_number',
                  "emergency_contact_number", "emergency_contact_person"]


class MemberSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()

    class Meta:
        extra_kwargs = {
            "team_id": {"required": True},
        }


    def validate_team_id(self, value):

        if value:
            try:
                value = EmergencyResponseTeam.objects.get(id=value)
            except EmergencyResponseTeam.DoesNotExist:
                raise serializers.ValidationError("Team does not exist")
            return value


class EmergencyResponseTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyResponseTeam
        fields = ['team_name']


class EmergencyResponseTeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyResponseTeam
        fields = ['team_name', 'members']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        context = self.context
        if isinstance(instance, Citizen):
            return CitizenListSerializer(instance, context=context).data
        elif isinstance(instance, EmergencyResponder):
            return EmergencyResponderListSerializer(instance, context=context).data
        return super().to_representation(instance)
