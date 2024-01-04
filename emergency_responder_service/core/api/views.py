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
from rest_framework import status

from django.http import HttpRequest

from rest_framework.permissions import IsAuthenticated
from core.authentication import TokenAuthentication

from core.models import EmergencyResponder, EmergencyResponseTeam,Resource,Alert,EmergencyAction,Messages
from api.serializers import (
    EmergencyResponderSerializer,
    CreateEmergencyResponseTeamSerializer,
    EmergencyResponseTeamSerializer,
    AddOrRemoveMemberSerializer,
    AlertSerializer,
    EmergencyActionSerializer,
    MessagesSerializer,
    ResourceSerializer,
    ResourceCreateSerializer,
    RemoveResourceSerializer
)


class EmergencyResponseViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
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
    
    def destroy(self, request, *args, **kwargs):
        team = self.get_object()
        team.is_active = False
        team.save()

        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["post"], url_path="add-member")
    def add_member(self, request, pk=None):
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
        
        team = self.get_object()
        serializer = ResourceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resource = serializer.save(commit=False)
        resource.team = team
        resource.save()

        return Response({"detail": "Resource added to the team"},status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="remove-resource")
    def remove_resource(self, request, pk=None):
        
        team = self.get_object()
        serializer = RemoveResourceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resource = serializer.validated_data["resource_id"]
        resource = Resource.objects.get(id=resource)
        resource.delete()

        return Response({"detail": "Resource removed from the team"},status=status.HTTP_200_OK)

    @action(detail=True, methods=["put","patch"], url_path="update-resource")
    def update_resource(self, request, pk=None):

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
        
        team = self.get_object()
        request.data["team"] = team.id
        serializer = EmergencyActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Emergency Action created","data":serializer.data},status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="messages")
    def messages(self, request, pk=None):
        
        team = self.get_object()
        messages = Messages.objects.filter(team=team)
        serializer = MessagesSerializer(messages, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="messages")
    def send_message(self, request, pk=None):
        
        team = self.get_object()
        request.data["team"] = team.id
        serializer = MessagesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Message sent"},status=status.HTTP_200_OK)

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