from django.urls import path,include


urlpatterns = [
    path('alerts', include('alerts.api.urls')),
]