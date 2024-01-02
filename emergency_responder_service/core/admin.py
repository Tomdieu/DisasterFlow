from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import EmergencyResponder,EmergencyResponseTeam,Location,Profile

# Register your models here.


@admin.register(EmergencyResponder)
class EmergencyResponderAdmin(admin.ModelAdmin):

    list_display = ['id','email','username','gender','date_of_birth','is_verified','specialization']

@admin.register(EmergencyResponseTeam)
class EmergencyResponseTeamAdmin(admin.ModelAdmin):

    list_display = ['id','team_name','specialization','is_active','is_verified','created_at']

@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):

    list_display = ['user','point','address','country','city','state']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ['user','location','skills','interest','is_online','last_activity']