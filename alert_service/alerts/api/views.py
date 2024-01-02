from rest_framework.response import Response

from rest_framework.mixins import CreateModelMixin,UpdateModelMixin,RetrieveModelMixin,ListModelMixin,DestroyModelMixin
# from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated,AllowAny
from alerts.authentication import TokenAuthentication

from alerts.api.serializers import AlertCreateSerializer,AlertListSerializer,UserReportCreateSerializer,UserReportListSerializer
from alerts.models import Alert,UserReport
from alerts.utils.alerts import get_alerts_within_location

# class LocationViewSet(GenericViewSet,CreateModelMixin,UpdateModelMixin,RetrieveModelMixin,ListModelMixin,DestroyModelMixin):
#     queryset = Location.objects.all()
#     serializer_class = LocationSerializer

class UserReportViewSet(GenericViewSet,CreateModelMixin,UpdateModelMixin,RetrieveModelMixin,ListModelMixin,DestroyModelMixin):
    
    queryset = UserReport.objects.all()
    serializer_class = UserReportCreateSerializer

    def get_serializer_class(self):

        if self.action in ['list','retrieve','my_reports']:
            return UserReportListSerializer
        
        return UserReportCreateSerializer
    
    permission_classes = [AllowAny]

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        user_report_object = self.get_object()
        if user_report_object.user != request.user:
            return Response({'message':'You are not allowed to update this report'},status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        user_report_object = self.get_object()
        if user_report_object.user != request.user:
            return Response({'message':'You are not allowed to update this report'},status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    @action(methods=['GET'],detail=False,url_path='my-reports')
    def my_reports(self,request):
        reports = UserReport.objects.filter(user__id=request.user.id)
        serializer = UserReportListSerializer(reports,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class AlertViewSet(GenericViewSet,CreateModelMixin,UpdateModelMixin,RetrieveModelMixin,ListModelMixin,DestroyModelMixin):
    queryset = Alert.objects.all()
    serializer_class = AlertCreateSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return AlertListSerializer
        return AlertCreateSerializer

    @action(methods=['GET'],detail=False,url_path='get-alerts-by-location')
    def get_alerts_by_location(self,request):
        location = request.query_params.get('location')
        if location:
            # alerts = Alert.objects.filter(location__id=location)
            alerts = get_alerts_within_location(place=location)
            serializer = AlertListSerializer(alerts,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message':'location is required'},status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'],detail=False,url_path='get-alerts-by-user')
    def get_alerts_by_user(self,request):   
        user_id = request.query_params.get('user_id')
        if user_id:
            alerts = Alert.objects.filter(created_by__id=user_id)
            serializer = AlertListSerializer(alerts,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message':'user_id is required'},status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'],detail=False,url_path='get-alerts-by-location-and-user')
    def get_alerts_by_location_and_user(self,request):
        location = request.query_params.get('location')
        user_id = request.query_params.get('user_id')
        if location and user_id:
            alerts = get_alerts_within_location(place=location,user_id=user_id)
            serializer = AlertListSerializer(alerts,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message':'location and user are required'},status=status.HTTP_400_BAD_REQUEST)
