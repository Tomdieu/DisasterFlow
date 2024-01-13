from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
# Register your models here.

from .models import Alert, Location, User, UserReport,Profile,Event


class ReadOnlyModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):
    list_display = ['point', 'address', 'country', 'city', 'state']

    list_filter = ['address', 'country', 'city', 'state']


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'severity', 'location', 'timestamp']
    list_filter = ['location', 'timestamp', 'type', 'severity', ]


@admin.register(UserReport)
class UserReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'location', 'impact', 'urgency', 'timestamp']
    list_filter = ['user', 'location', 'impact', 'urgency', 'timestamp']


@admin.register(User)
class UserAdmin(ReadOnlyModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'type', 'gender']
    list_filter = ['username', 'email', 'type', 'gender']

@admin.register(Profile)
class ProfileAdmin(ReadOnlyModelAdmin):

    list_display = ['user','location','skills']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id','event_type','data','timestamp']