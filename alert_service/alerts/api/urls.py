from rest_framework.routers import DefaultRouter

from .views import UserReportViewSet, AlertViewSet, LocationViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet)
router.register(r'user-reports', UserReportViewSet)
router.register(r'alerts', AlertViewSet)

urlpatterns = router.urls
