from django.contrib import admin

# Register your models here.

from .models import Alert, Location, Profile, User, UserReport

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):

    list_display = ['id', 'lat', 'lng', 'zip_code', 'locality']
    list_filter = ['zip_code', 'locality']

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'description','type','severity', 'location', 'timestamp']
    list_filter = ['location', 'timestamp','type''severity',]

@admin.register(UserReport)
class UserReportAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'title', 'description', 'location', 'impact', 'urgency', 'timestamp', 'updated_at']
    list_filter = ['user', 'location', 'impact', 'urgency', 'timestamp']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ['username','email','phone_number','type','gender']
    list_filter = ['username','email','type','gender']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ['user','location','skills','interests','is_online','last_activity']
    list_filter = ['user','location','skills','interests','is_online','last_activity']