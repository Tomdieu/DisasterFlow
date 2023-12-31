from rest_framework.routers import DefaultRouter

from .views import LocationViewSet,UserReportViewSet,AlertViewSet

router = DefaultRouter()
router.register(r'locations',LocationViewSet)
router.register(r'user-reports',UserReportViewSet)
router.register(r'alerts',AlertViewSet)

urlpatterns = router.urls