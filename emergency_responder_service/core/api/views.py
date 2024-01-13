from rest_framework.response import Response
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from core.authentication import TokenAuthentication

from core.models import EmergencyResponder, EmergencyResponseTeam,Resource,Alert,EmergencyAction,Messages,EmergencyNotification
from .serializers import (
    EmergencyResponderSerializer,
    CreateEmergencyResponseTeamSerializer,
    EmergencyResponseTeamSerializer,
    AddOrRemoveMemberSerializer,
    AlertSerializer,
    EmergencyActionSerializer,
    MessagesSerializer,
    ResourceSerializer,
    ResourceCreateSerializer,
    RemoveResourceSerializer,
    EmergencyNotificationSerializer,
    LocationSerializer
)


class EmergencyResponderViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = EmergencyResponderSerializer
    queryset = EmergencyResponder.objects.all()
    authentication_classes = [TokenAuthentication]

    def get_serializer_class(self):
        if self.action in ["add_member", "remove_member"]:
            return AddOrRemoveMemberSerializer
        return EmergencyResponderSerializer


class EmergencyResponseTeamViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = EmergencyResponseTeam.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateEmergencyResponseTeamSerializer
        elif self.action == ["list", "update", "partial_update", "retrieve"]:
            return EmergencyResponseTeamSerializer
        elif self.action == "add_member":
            return AddOrRemoveMemberSerializer
        elif self.action == "remove_member":
            return AddOrRemoveMemberSerializer
        elif self.action == "add_resource":
            return ResourceCreateSerializer
        elif self.action == "update_resource":
            return ResourceSerializer
        elif self.action == "emergency_action":
            return EmergencyActionSerializer
        elif self.action == "emergency_actions":
            return EmergencyActionSerializer
        elif self.action == "messages":
            return MessagesSerializer
        elif self.action == "send_message":
            return MessagesSerializer
        elif self.action == "notifications":
            return EmergencyNotificationSerializer
    
    def destroy(self, request, *args, **kwargs):
        team = self.get_object()
        team.is_active = False
        team.save()

        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["post"], url_path="add-member")
    def add_member(self, request, pk=None):

        """
        This route is use to add a new member to an emergency responder team
        """
        
        team = self.get_object()
        serializer = AddOrRemoveMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = serializer.validated_data["emergency_responder_id"]
        # check if member is already in team
        if member in team.members.all():
            return Response(
                {"detail": "Emergency Responder is already in the team"},
                status=400,
            )
        team.members.add(member)
        team.save()
        return Response({"detail": "Emergency Responder added to the team"},status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="remove-member")
    def remove_member(self, request, pk=None):
        """
        This roiute is use to remove a member from an emergency responder team
        """

        team = self.get_object()
        serializer = AddOrRemoveMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = serializer.validated_data["emergency_responder_id"]
        # check if member is already in team
        if member not in team.members.all():
            return Response(
                {"detail": "Emergency Responder is not in the team"}, status=400
            )
        team.members.remove(member)
        team.save()
        return Response({"detail": "Emergency Responder removed from the team"},status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="add-resource")
    def add_resource(self, request, pk=None):
        """
        This route is use to add a resource to an Emergency Responder Team
        """
        
        team = self.get_object()
        serializer = ResourceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resource = serializer.save(commit=False)
        resource.team = team
        resource.save()

        return Response({"detail": "Resource added to the team"},status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="remove-resource")
    def remove_resource(self, request, pk=None):
        """This Route is use to remove a resource from an emergency responder team"""

        team = self.get_object()
        serializer = RemoveResourceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resource = serializer.validated_data["resource_id"]
        resource = Resource.objects.get(id=resource)
        resource.delete()

        return Response({"detail": "Resource removed from the team"},status=status.HTTP_200_OK)

    @action(detail=True, methods=["put","patch"], url_path="update-resource")
    def update_resource(self, request, pk=None):
        """This route is use to update the resource from an emergency responder team"""
        team = self.get_object()
        serializer = ResourceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resource = serializer.validated_data["id"]
        data = serializer.validated_data
        resource = Resource.objects.get(id=resource)

        for key,value in data.items():
            setattr(resource,key,value)
        resource.save()

        updated_resource = ResourceSerializer(resource)

        return Response({"detail": "Resource updated","data":updated_resource.data},status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="emergency-action")
    def emergency_action(self, request, pk=None):
        """This route is use to take an action by an emergency responder team base on an alert"""
        team = self.get_object()
        request.data["team"] = team.id
        serializer = EmergencyActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Emergency Action created","data":serializer.data},status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('status',openapi.IN_QUERY,description="status of the emergency action either in `In Progress`,`Completed`, or `Cancelled`",type=openapi.TYPE_INTEGER,required=False)
        ]
    )
    @action(detail=True,methods=['get'],url_path='emergency-actions')
    def emergency_actions(self,request,pk=None):
        """This route is use to list all the emergency actions taken by a team"""

        team = self.get_object()
        status = request.query_params.get('status')
        emergency_actions = []
        if status:
            emergency_actions = EmergencyAction.objects.filter(team=team,status=status)
        else:
            emergency_actions = EmergencyAction.objects.filter(team=team)
        serializer = EmergencyActionSerializer(emergency_actions,many=True,context={'request':request})

        return Response(serializer.data,status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: MessagesSerializer(many=True)})
    @action(detail=True, methods=["get"], url_path="messages")
    def messages(self, request, pk=None):
        """This route is use to list all the messages from an emergency reponder team"""
        team = self.get_object()
        messages = Messages.objects.filter(team=team)
        serializer = MessagesSerializer(messages, many=True,context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="send-messages")
    def send_message(self, request, pk=None):
        "This route is use to send message in an emergency responder chat"
        team = self.get_object()
        request.data["team"] = team.id
        serializer = MessagesSerializer(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Message sent"},status=status.HTTP_200_OK)
    
    @action(detail=True,methods=['get'])
    def notifications(self,request,pk=None):

        team = self.get_object()
        notifications = EmergencyNotification.objects.filter(team=team)

        serializer = EmergencyNotificationSerializer(notifications,many=True,context={'request':request})

        return Response(serializer.data,status=status.HTTP_200_OK)

class AlertViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

class EmergencyActionViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = EmergencyAction.objects.all()
    serializer_class = EmergencyActionSerializer


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='origin',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Origin location in the format lat|lng or simply address name',
                required=False,
            ),
            openapi.Parameter(
                name='destination',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Destination location in the format lat|lng or simplce address name',
                required=False,
            ),
        ],
    )
    @action(detail=True,methods=['get'])
    def path(self,request,pk=None):
        from core.utils import Geoapify,Feature
        import re

        lat_lng_pattern = re.compile(r'^[-+]?\d*\.\d+|[-+]?\d+$')
        address_name_pattern = re.compile(r'^[a-zA-Z0-9\s]+$')


        geoapify = Geoapify()

        origin = request.query_params.get('origin',None)
        destination = request.query_params.get('destination',None)

        emergency_action = self.get_object()

        alert = emergency_action.alert
        team_location = emergency_action.team.location
        

        if origin and destination:

            if lat_lng_pattern.match(origin) and lat_lng_pattern.match(destination):
                origin = f'{origin[0]}|{origin[1]}'
                destination = f'{destination[0]}|{destination[1]}'

                path = geoapify.get_routes_between_locations(origin,destination)

                return Response(path,status=status.HTTP_200_OK)
            else:

                origin = geoapify.forward_geocode(origin)
                destination = geoapify.forward_geocode(destination)

                origin = [origin.results[0].lat,origin.results[0].lon]
                destination = [destination.results[0].lat,destination.results[0].lon]

                origin = f'{origin[0]}|{origin[1]}'
                destination = f'{destination[0]}|{destination[1]}'

                path = geoapify.get_routes_between_locations(origin,destination)

                return Response(path,status=status.HTTP_200_OK)
        
        if origin and not destination:

            origin = geoapify.forward_geocode(origin)

            origin = [origin.results[0].lat,origin.results[0].lon]
            
            alert_location = alert.location
            alert_location_serializer = LocationSerializer(alert_location)
            alert_location_data = Feature(**alert_location_data.data)
            
            destination = [alert_location_data.geometry.coordinates[1],alert_location_data.geometry.coordinates[0]]

            origin = f'{origin[0]}|{origin[1]}'
            destination = f'{destination[0]}|{destination[1]}'
            

            path = geoapify.get_routes_between_locations(origin,destination)

            return Response(path,status=status.HTTP_200_OK)
        
        if destination and not origin:
            
            destination = geoapify.forward_geocode(destination)

            destination = [destination.results[0].lat,destination.results[0].lon]
            
            alert_location = alert.location
            alert_location_serializer = LocationSerializer(alert_location)
            alert_location_data = Feature(**alert_location_data.data)
            
            origin = [alert_location_data.geometry.coordinates[1],alert_location_data.geometry.coordinates[0]]

            origin = f'{origin[0]}|{origin[1]}'
            destination = f'{destination[0]}|{destination[1]}'
            

            path = geoapify.get_routes_between_locations(origin,destination)

            return Response(path,status=status.HTTP_200_OK)

        


        
        return Response(path,status=status.HTTP_200_OK)
    