# from django.db import models
from django.contrib.gis.db import models
from .disaster_types import TYPES
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

class Profile(models.Model):
    user = models.OneToOneField(EmergencyResponder, on_delete=models.CASCADE, primary_key=True, related_name="profile")
    location = models.CharField(max_length=255, blank=True, null=True)
    skills = models.CharField(help_text=_("each skill Should be separated by `,`"), max_length=255, null=True,
                              blank=True)
    interest = models.TextField(null=True, blank=True)

    is_online = models.BooleanField(default=False)
    last_activity = models.DateTimeField(blank=True,null=True)

    class Meta:
        pass

    def __str__(self):
        return f"{self.user} - profile"
    
class Location(models.Model):
    user = models.OneToOneField(EmergencyResponder, on_delete=models.CASCADE, primary_key=True, related_name="location")
    point = models.PointField(blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100)


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
    
class Messages(models.Model):

    "Here messages are sent and received by emergency responders"
    team = models.ForeignKey(EmergencyResponseTeam, on_delete=models.CASCADE,related_name="messages")
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
        ("Unavailable","Unavailable"),
        ("Damaged", "Damaged"),
        ("Lost", "Lost"),
    ]

    RESOURCE_TYPE = [
        ("Fire Truck", "Fire Truck"),
        ("Ambulance", "Ambulance"),
        ("Police Car", "Police Car"),
        ("Helicopter", "Helicopter"),
        ("Boat", "Boat"),
        ("Motorcycle", "Motorcycle"),
        ("Fire Extinguisher", "Fire Extinguisher"),
        ("Fire Hose", "Fire Hose"),
        ("Fire Hydrant", "Fire Hydrant"),
        ("Fire Axe", "Fire Axe"),
        ("Fire Blanket", "Fire Blanket"),
        ("Fire Bucket", "Fire Bucket"),
        ("Fire Escape Ladder", "Fire Escape Ladder"),
        ("Fire Sprinkler", "Fire Sprinkler"),
        ("Fire Alarm", "Fire Alarm"),
        ("Fire Alarm Control Panel", "Fire Alarm Control Panel"),
        ("Fire Extinguisher Sign", "Fire Extinguisher Sign"),
        ("Fire Hose Sign", "Fire Hose Sign"),
        ("Fire Exit Sign", "Fire Exit Sign"),
        ("Fire Assembly Point Sign", "Fire Assembly Point Sign"),
        ("Fire Alarm Bell", "Fire Alarm Bell"),
        ("Fire Alarm Sounder", "Fire Alarm Sounder"),
        ("Fire Alarm Strobe", "Fire Alarm Strobe"),
        ("Fire Alarm Pull Station", "Fire Alarm Pull Station"),
        ("Fire Alarm Control Panel", "Fire Alarm Control Pane"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=255,choices=RESOURCE_TYPE)
    quantity = models.IntegerField(default=0)
    avaialable = models.BooleanField(default=True)
    status = models.CharField(max_length=255,choices=STATUS, blank=True, null=True)
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

    title = models.CharField(max_length=255)

    description = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TYPES)
    severity = models.CharField(max_length=100, choices=SEVERITY)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField()
    audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES)

    def __str__(self):
        return f"{self.title} - {self.type}"
    
class EmergencyAction(models.Model):
    "Here emergency action is a situation that poses an immediate risk to health, life, property, or environment."

    STATUS = [
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    ACTION_TYPE = [
        ("Rescue", "Rescue"),
        ("Medical Assistance","Medical Assistance"),
        ("Evacuation", "Evacuation"),
        ("First Aid", "First Aid"),
        ("Fire Fighting", "Fire Fighting"),
        ("Crime Control", "Crime Control"),
        ("Other", "Other"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    action_type = models.CharField(max_length=255,choices=ACTION_TYPE)
    status = models.CharField(max_length=255,choices=STATUS, blank=True, null=True)
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