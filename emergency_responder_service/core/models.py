# from django.db import models
from django.contrib.gis.db import models

from django.utils.translation import gettext_lazy as _

# Create your models here.

SPECIALIZATION_CHOICES = [
        ("Firefighting", "Firefighting"),
        ("Law Enforcement", "Law Enforcement"),
        ("Emergency Medical Services (EMS)", "Emergency Medical Services (EMS)"),
        ("Search and Rescue", "Search and Rescue"),
        (
            "Hazardous Materials (HazMat) Response",
            "Hazardous Materials (HazMat) Response",
        ),
        ("Technical Rescue", "Technical Rescue"),
        ("Urban Search and Rescue (USAR)", "Urban Search and Rescue (USAR)"),
        ("Critical Incident Response", "Critical Incident Response"),
        ("Medical Specialization", "Medical Specialization"),
        ("Disaster Response and Recovery", "Disaster Response and Recovery"),
        ("Communications and Coordination", "Communications and Coordination"),
        ("Aviation Rescue", "Aviation Rescue"),
    ]


class EmergencyResponder(models.Model):
    
    id = models.BigIntegerField(primary_key=True)
    email = models.EmailField(_("email address"), unique=True)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    username = models.CharField(max_length=120)
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact_person = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    specialization = models.CharField(
        max_length=255, choices=SPECIALIZATION_CHOICES, null=True, blank=True
    )


class EmergencyResponseTeam(models.Model):
    team_name = models.CharField(max_length=255)
    address = models.CharField(max_length=100, blank=True, null=True)
    point = models.PointField(blank=True, null=True)
    members = models.ManyToManyField(EmergencyResponder, blank=True)
    specialization = models.CharField(
        max_length=255, choices=SPECIALIZATION_CHOICES, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.team_name
