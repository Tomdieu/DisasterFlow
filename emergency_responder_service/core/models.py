# from django.db import models
from django.contrib.gis.db import models
from .disaster_types import TYPES
from django.utils.translation import gettext_lazy as _
import uuid

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
    class Types(models.TextChoices):
        CITIZEN = "Citizen", "Citizen"
        EMERGENCY_RESPONDER = "EmergencyResponder", "Emergency Responder"
        ADMIN = "administrator", "Administrator"
        
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other")
    ]
    id = models.BigIntegerField(primary_key=True)
    email = models.EmailField(_("email address"), unique=True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.CharField(max_length=255,blank=True,null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    username = models.CharField(max_length=120,blank=True,null=True)
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    type = models.CharField(max_length=255, choices=Types.choices, default=Types.CITIZEN)
    emergency_contact_number = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact_person = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    specialization = models.CharField(
        max_length=255, choices=SPECIALIZATION_CHOICES, null=True, blank=True
    )


class Profile(models.Model):
    user = models.OneToOneField(
        EmergencyResponder,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile",
    )
    location = models.CharField(max_length=255, blank=True, null=True)
    skills = models.CharField(
        help_text=_("each skill Should be separated by `,`"),
        max_length=255,
        null=True,
        blank=True,
    )
    interest = models.TextField(null=True, blank=True)

    is_online = models.BooleanField(default=False)
    last_activity = models.DateTimeField(blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return f"{self.user} - profile"


class Location(models.Model):
    user = models.OneToOneField(
        EmergencyResponder,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="location",
    )
    point = models.PointField(blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    

class AlertLocation(models.Model):
    point = models.PointField(blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)


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
    created_by = models.ForeignKey(EmergencyResponder, on_delete=models.CASCADE,related_name="teams")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.team_name


class Messages(models.Model):
    "Here messages are sent and received by emergency responders"
    team = models.ForeignKey(
        EmergencyResponseTeam, on_delete=models.CASCADE, related_name="messages"
    )
    id = models.BigIntegerField(primary_key=True)
    sender = models.ForeignKey(
        EmergencyResponder, on_delete=models.CASCADE, related_name="messages"
    )
    text = models.TextField()
    is_deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} - {self.text}"


class Resource(models.Model):
    "Here resources belongs to a team of emergency responders which can be use in emergency situations"

    STATUS = [
        ("Available", "Available"),
        ("In Use", "In Use"),
        ("Unavailable", "Unavailable"),
        ("Damaged", "Damaged"),
        ("Lost", "Lost"),
    ]

    RESOURCE_TYPE = {
        "Firefighting": {
            "fire trucks and engines": "Fire Trucks and Engines",
            "water hoses and hydrants": "Water Hoses and Hydrants",
            "fire retardant materials": "Fire Retardant Materials",
            "human resources": "Firefighters and Emergency Personnel",
        },
        "Law Enforcement": {
            "police vehicles": "Police Vehicles",
            "communication devices (radios)": "Communication Devices (Radios)",
            "protective gear (body armor, helmets)": "Protective Gear (Body Armor, Helmets)",
            "human resources": "Law Enforcement Officers",
        },
        "Emergency Medical Services (EMS)": {
            "ambulances": "Ambulances",
            "medical supplies and equipment": "Medical Supplies and Equipment",
            "emergency medical personnel": "Emergency Medical Personnel",
            "human resources": "Paramedics and Medical Teams",
        },
        "Search and Rescue": {
            "search and rescue dogs": "Search and Rescue Dogs",
            "drones": "Drones",
            "rope and climbing gear": "Rope and Climbing Gear",
            "human resources": "Search and Rescue Teams",
        },
        "Hazardous Materials (HazMat) Response": {
            "HazMat suits": "HazMat Suits",
            "decontamination equipment": "Decontamination Equipment",
            "specialized detection devices": "Specialized Detection Devices",
            "human resources": "HazMat Response Teams",
        },
        "Technical Rescue": {
            "rope rescue systems": "Rope Rescue Systems",
            "specialized tools (jaws of life)": "Specialized Tools (Jaws of Life)",
            "rescue boats": "Rescue Boats",
            "human resources": "Technical Rescue Teams",
        },
        "Urban Search and Rescue (USAR)": {
            "heavy machinery (cranes, excavators)": "Heavy Machinery (Cranes, Excavators)",
            "structural collapse detection tools": "Structural Collapse Detection Tools",
            "listening devices for detecting survivors": "Listening Devices for Detecting Survivors",
            "human resources": "Urban Search and Rescue Teams",
        },
        "Critical Incident Response": {
            "command centers": "Command Centers",
            "crisis management software": "Crisis Management Software",
            "emergency response plans": "Emergency Response Plans",
            "human resources": "Emergency Response Personnel",
        },
        "Medical Specialization": {
            "mobile medical units": "Mobile Medical Units",
            "advanced life support equipment": "Advanced Life Support Equipment",
            "specialized medical personnel": "Specialized Medical Personnel",
            "human resources": "Medical Teams",
        },
        "Disaster Response and Recovery": {
            "temporary shelters": "Temporary Shelters",
            "disaster recovery vehicles": "Disaster Recovery Vehicles",
            "cleanup and rebuilding tools": "Cleanup and Rebuilding Tools",
            "human resources": "Recovery and Rebuilding Teams",
        },
        "Communications and Coordination": {
            "communication networks": "Communication Networks",
            "satellite phones": "Satellite Phones",
            "incident management software": "Incident Management Software",
            "human resources": "Communication and Coordination Personnel",
        },
        "Aviation Rescue": {
            "helicopters and aircraft": "Helicopters and Aircraft",
            "aerial surveillance equipment": "Aerial Surveillance Equipment",
            "emergency parachuting equipment": "Emergency Parachuting Equipment",
            "human resources": "Aviation Rescue Teams",
        },
    }

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=255, choices=RESOURCE_TYPE)
    quantity = models.IntegerField(default=0)
    avaialable = models.BooleanField(default=True)
    status = models.CharField(max_length=255, choices=STATUS, blank=True, null=True)
    team = models.ForeignKey(
        EmergencyResponseTeam, on_delete=models.CASCADE, related_name="resources"
    )
    timestamp = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


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

    image = models.TextField(blank=True,null=True)
    type = models.CharField(max_length=255, choices=TYPES)
    severity = models.CharField(max_length=100, choices=SEVERITY)
    location = models.ForeignKey(AlertLocation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    created_by = models.IntegerField("User id",help_text="This is the id of the user who created the alert")
    audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES)

    def __str__(self):
        return f"Alert : {self.type} severity : {self.severity}"
    
class EmergencyNotification(models.Model):

    STATUS = [
        ('pending','pending'),
        ('accept','accept'),
        ('cancel','cancel')
    ]

    alert = models.ForeignKey(Alert,on_delete=models.CASCADE)
    team = models.ForeignKey(EmergencyResponseTeam,on_delete=models.CASCADE,related_name="notifications")
    message = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=20,choices=STATUS,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):

        return f"Alert Notification {self.alert} for {self.team}"



class EmergencyAction(models.Model):
    "Here emergency action is a situation that poses an immediate risk to health, life, property, or environment."

    STATUS = [
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    ACTION_TYPE = [
        ("Rescue", "Rescue"),
        ("Medical Assistance", "Medical Assistance"),
        ("Evacuation", "Evacuation"),
        ("First Aid", "First Aid"),
        ("Fire Fighting", "Fire Fighting"),
        ("Crime Control", "Crime Control"),
        ("Other", "Other"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    action_type = models.CharField(max_length=255, choices=ACTION_TYPE)
    status = models.CharField(max_length=255, choices=STATUS,default="In Progress", blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    point = models.PointField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    alert = models.ForeignKey(
        Alert, on_delete=models.CASCADE, related_name="emergency_actions"
    )
    team = models.ForeignKey(
        EmergencyResponseTeam, on_delete=models.CASCADE, related_name="emergencies"
    )
    resources = models.ManyToManyField(Resource, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.location = self.alert.location.address
        self.point = self.alert.location.point
        super().save(*args, **kwargs)


class Event(models.Model):
    # This represent the event store in the database
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self) -> str:
        return f"{self.event_type} - {self.timestamp}"