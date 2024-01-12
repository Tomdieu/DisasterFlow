from rest_framework import serializers
from rest_framework import fields
from accounts.models import Profile, Citizen, EmergencyResponder, User,Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['user','lat', 'lng', 'address', 'country', 'city', 'state']

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
        fields = ['user','location', 'skills', 'interest', 'is_online', 'last_activity']


class CitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = ['username', 'email', 'type','gender', 'date_of_birth', 'profile_image', 'phone_number',"password"]

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
    location = LocationSerializer()

    class Meta:
        model = Citizen
        fields = ['id','username', 'email', 'type',"gender", 'date_of_birth', 'profile_image','phone_number','profile','location']


class EmergencyResponderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyResponder
        fields = ['username', 'email', 'type',"gender","specialization", 'date_of_birth', 'profile_image', 'phone_number',"password"]

        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": True,
            },
            "email": {
                "required": True,
            },
        }


class EmergencyResponderSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyResponder
        fields = ['id','username', 'email', 'type',"gender","specialization", 'date_of_birth', 'profile_image',"gender", 'phone_number']

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
    location = LocationSerializer()

    class Meta:
        model = EmergencyResponder
        fields = ['id','username', 'email', 'type',"gender","specialization", 'date_of_birth', 'profile_image',"gender", 'phone_number','profile','location']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    location = LocationSerializer()

    class Meta:
        model = User
        # fields = '__all__'

        exclude = ['groups','user_permissions','is_staff','is_active']

        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    def to_representation(self, instance):
        context = self.context
        if isinstance(instance, Citizen):
            return CitizenListSerializer(instance, context=context).data
        elif isinstance(instance, EmergencyResponder):
            return EmergencyResponderListSerializer(instance, context=context).data
        return super().to_representation(instance)
