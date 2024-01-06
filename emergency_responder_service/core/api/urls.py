from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r"emergency-responders", views.EmergencyResponderViewSet)
router.register(r"emergency-responder-teams", views.EmergencyResponseTeamViewSet)
router.register(r"alerts", views.AlertViewSet)
router.register(r"emergency-actions", views.EmergencyActionViewSet)


urlpatterns = router.urls