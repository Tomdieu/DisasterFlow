from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, Event, Citizen, EmergencyResponder, Location#,EmergencyResponseTeam

from django.contrib.auth import get_user_model

# Register your models here.

User = get_user_model()


class LocationInline(admin.StackedInline):
    extra = 1
    model = Location


class ProfileInline(admin.StackedInline):
    extra = 1
    model = Profile


# @admin.register(User)
# class UserAdmin(BaseUserAdmin):

#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         (
#             "Personal info",
#             {"fields": ("username", "phone_number", "first_name", "last_name","date_of_birth","profile_image")},
#         ),
#         (
#             "Permissions",
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     "groups",
#                     "user_permissions",
#                 ),
#             },
#         ),
#         ("Important dates", {"fields": ("last_login", "date_joined")}),
#     )

#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": (
#                     "username",

#                     "email",
#                     "phone_number",
#                     "date_of_birth",
#                     "profile_image",
#                     "password1",
#                     "password2",
#                 ),
#             },
#         ),
#     )
#     list_per_page = 25
#     search_fields = ("username", "first_name", "last_name", "email", "phone_number")
#     list_display = ("username", "email", "first_name", "last_name", "is_staff")
#     list_filter = ("is_staff", "is_superuser", "is_active", "groups")


#     inlines = [ProfileInline]


@admin.register(Citizen)
class CitizenAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password",)}),
        (
            "Personal info",
            {"fields": ("username", "phone_number", "first_name", "last_name", "date_of_birth", "profile_image")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "phone_number",
                    "date_of_birth",
                    "profile_image",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_per_page = 25
    search_fields = ("username", "first_name", "last_name", "email", "phone_number")
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    inlines = [ProfileInline, LocationInline]


@admin.register(EmergencyResponder)
class EmergencyResponderAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password",)}),
        (
            "Personal info",
            {"fields": ("username", "phone_number", "first_name", "last_name", "date_of_birth", "profile_image",
                        "emergency_contact_number")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "phone_number",
                    "date_of_birth",
                    "profile_image",
                    "emergency_contact_number",
                    "emergency_contact_person",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    list_per_page = 25
    search_fields = ("username", "first_name", "last_name", "email", "phone_number")
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    inlines = [ProfileInline, LocationInline]


# admin.site.register(EmergencyResponseTeam)
admin.site.register(Event)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'skills', 'last_activity', 'is_online']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['user', 'lat', 'lng', 'address', 'country', 'city', 'state']
