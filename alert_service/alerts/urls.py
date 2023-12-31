from django.urls import path,include

urlpatterns = [
    path('api', include('alerts.api.urls')),
]