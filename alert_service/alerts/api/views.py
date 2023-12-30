from rest_framework.response import Response

from rest_framework.mixins import CreateModelMixin,UpdateModelMixin,RetrieveModelMixin,ListModelMixin,DestroyModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from alerts.api.serializers import AlertCreateSerializer,AlertListSerializer,LocationSerializer,UserReportCreateSerializer,UserSerializer,ProfileSerializer
from alerts.models import Alert,Location,UserReport,User,Profile

class LocationViewSet(GenericViewSet,CreateModelMixin,UpdateModelMixin,RetrieveModelMixin,ListModelMixin,DestroyModelMixin):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class UserReportViewSet(GenericViewSet,CreateModelMixin,UpdateModelMixin,RetrieveModelMixin,ListModelMixin,DestroyModelMixin):
    queryset = UserReport.objects.all()
    serializer_class = UserReportCreateSerializer

class AlertViewSet(GenericViewSet,CreateModelMixin,UpdateModelMixin,RetrieveModelMixin,ListModelMixin,DestroyModelMixin):
    queryset = Alert.objects.all()
    serializer_class = AlertCreateSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return AlertListSerializer
        return AlertCreateSerializer

    @action(methods=['GET'],detail=False,url_path='get-alerts-by-location')
    def get_alerts_by_location(self,request):
        location_id = request.query_params.get('location_id')
        if location_id:
            alerts = Alert.objects.filter(location__id=location_id)
            serializer = AlertListSerializer(alerts,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message':'location_id is required'},status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'],detail=False,url_path='get-alerts-by-user')
    def get_alerts_by_user(self,request):
        user_id = request.query_params.get('user_id')
        if user_id:
            alerts = Alert.objects.filter(user__id=user_id)
            serializer = AlertListSerializer(alerts,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message':'user_id is required'},status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'],detail=False,url_path='get-alerts-by-location-and-user')
    def get_alerts_by_location_and_user(self,request):
        location_id = request.query_params.get('location_id')
        user_id = request.query_params.get('user_id')
        if location_id and user_id:
            alerts = Alert.objects.filter(location__id=location_id,user__id=user_id)
            serializer = AlertListSerializer(alerts,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message':'location_id and user_id are required'},status=status.HTTP_400_BAD_REQUEST)
