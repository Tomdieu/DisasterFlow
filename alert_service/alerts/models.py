# from django.db import models
from django.utils import timezone
from django.contrib.gis.db import models
from .disaster_types import TYPES

# Create your models here.


class Location(models.Model):
    point = models.PointField()
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.lat} - {self.lng}"


class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    profile_image = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


    def __str__(self):
        return f"{self.username} - {self.type}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    skills = models.CharField(max_length=255)
    interests = models.CharField(max_length=255)

    is_online = models.BooleanField(default=False)
    last_activity = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.skills}"



class UserReport(models.Model):
    IMPACT = [
        ("low", "Low"),
        ("moderate", "Moderate"),
        ("high", "High"),
    ]

    URGENCY = [
        ("low", "Low"),
        ("moderate", "Moderate"),
        ("high", "High"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=255, choices=TYPES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    impact = models.CharField(max_length=255, choices=IMPACT,default="low")
    urgency = models.CharField(max_length=255, choices=URGENCY,default="low")

    def __str__(self) -> str:
        return f"{self.title} - {self.user.username}"


class Alert(models.Model):
    

    SEVERITY = [
        ("low", "Low"),
        ("moderate", "Moderate"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    AUDIENCE_CHOICES = [
        ("public", "Public"),
        ("emergency_responders", "Emergency Responders"),
    ]

    title = models.CharField(max_length=255)

    description = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TYPES)
    severity = models.CharField(max_length=100, choices=SEVERITY)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES)

    def __str__(self):
        return f"{self.title} - {self.type}"
