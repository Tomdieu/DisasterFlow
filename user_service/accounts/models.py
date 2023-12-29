from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid

from accounts.patterns import Visitor


# Create your models here.

class User(AbstractUser):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other")
    ]

    class Types(models.TextChoices):
        CITIZEN = "Citizen", "Citizen"
        EMERGENCY_RESPONDER = "EmergencyResponder", "Emergency Responder"
        ADMIN = "administrator", "Administrator"

    email = models.EmailField(_("email address"), unique=True)

    type = models.CharField(max_length=255, choices=Types.choices, default=Types.CITIZEN)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)

    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile_images/", null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    is_emergency_responder = models.BooleanField(default=False)
    is_citizen = models.BooleanField(default=False)

    # is_online = models.BooleanField(default=False)
    # last_activity = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def update_last_activity(self):
        self.last_activity = timezone.now()
        self.save()

    def accept(self, visitor: Visitor):
        pass

    def __str__(self):
        return f"{self.username} - {self.type}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="profile")
    location = models.CharField(max_length=255, null=True, blank=True)
    skills = models.CharField(help_text=_("each skill Should be separated by `,`"), max_length=255, null=True,
                              blank=True)
    interest = models.TextField(null=True, blank=True)

    is_online = models.BooleanField(default=False)
    last_activity = models.DateTimeField(default=timezone.now)

    class Meta:
        pass

    def __str__(self):
        return f"{self.user} - profile"


class Citizen(User):
    home_address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        pass

    def save(self, *args, **kwargs):
        self.is_citizen = True
        self.type = User.Types.CITIZEN
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.type}"

    def accept(self, visitor: Visitor):
        visitor.visit_citizen(self)


class EmergencyResponder(User):
    emergency_contact_number = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact_person = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        pass

    def save(self, *args, **kwargs):
        self.is_emergency_responder = True
        self.type = User.Types.EMERGENCY_RESPONDER
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.type}"

    def accept(self, visitor: Visitor):
        visitor.visit_emergency_responder(self)


class EmergencyResponseTeam(models.Model):
    emergency_responder = models.OneToOneField(EmergencyResponder, on_delete=models.CASCADE, related_name="team")
    team_name = models.CharField(max_length=50)
    members = models.ManyToManyField(EmergencyResponder)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Emergency Response Team: {self.team_name}"



class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self) -> str:
        return f"{self.event_type} - {self.timestamp}"
