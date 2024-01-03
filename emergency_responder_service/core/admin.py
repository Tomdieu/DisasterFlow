from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import EmergencyResponder,EmergencyResponseTeam,Location,Profile,Alert,EmergencyAction,Messages,Resource

# Register your models here.

class ReadOnlyModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(EmergencyResponder)
class EmergencyResponderAdmin(ReadOnlyModelAdmin):

    list_display = ['id','email','username','gender','date_of_birth','is_verified','specialization']

@admin.register(EmergencyResponseTeam)
class EmergencyResponseTeamAdmin(admin.ModelAdmin):

    list_display = ['id','team_name','specialization','is_active','is_verified','created_at']

@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):

    list_display = ['user','point','address','country','city','state']

@admin.register(Profile)
class ProfileAdmin(ReadOnlyModelAdmin):

    list_display = ['user','location','skills','interest','is_online','last_activity']

@admin.register(Alert)
class AlertAdmin(ReadOnlyModelAdmin):
    list_display = ['title','description','type','severity','location']

@admin.register(EmergencyAction)
class EmergencyActionAdmin(admin.ModelAdmin):

    list_display = ['id','alert','team','created_at']

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    pass
    list_display = ['id','team','sender','text','is_deleted','created_at']

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):

    list_display = ['id','name','quantity','type','avaialable','created_at']