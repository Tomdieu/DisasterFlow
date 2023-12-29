from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views

userRouter = DefaultRouter()

userRouter.register("login",views.LoginViewSet,basename="login")
userRouter.register("citizen",views.CitizenViewSet,basename="citizens")
userRouter.register("emergency-responder",views.EmergencyResponderViewSet,basename="emergency-responder")
userRouter.register("user",views.UserViewSet,basename="user")


urlpatterns = [
    path('signup/citizen/',views.RegisterCitizenResponderViewSet.as_view({'post':'create'})),
    path('signup/emergency-responder/',views.RegisterEmergencyResponderViewSet.as_view({'post':'create'})),
]

urlpatterns += userRouter.urls
