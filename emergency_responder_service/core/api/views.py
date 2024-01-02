from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin,ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated
from core.authentication import TokenAuthentication

from core.models import EmergencyResponder,EmergencyResponseTeam
from api.serializers import EmergencyResponderSerializer,CreateEmergencyResponseTeamSerializer,EmergencyResponseTeamSerializer,AddOrRemoveMemberSerializer

class EmergencyResponserViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    
    serializer_class = EmergencyResponderSerializer
    queryset = EmergencyResponder.objects.all()
    authentication_classes = [TokenAuthentication]

    def get_serializer_class(self):
            
        if self.action in ['add_member','remove_member']:
            return AddOrRemoveMemberSerializer
        return EmergencyResponderSerializer
    

class EmergencyResponseTeamViewSet(CreateModelMixin,ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericViewSet):

    queryset = EmergencyResponseTeam.objects.all()

    def get_serializer_class(self):

        if self.action == "create":
            return CreateEmergencyResponseTeamSerializer
        elif self.action == ["list","update","partial_update","retrieve"]:
            return EmergencyResponseTeamSerializer
        elif self.action == "add_member":
            return AddOrRemoveMemberSerializer
        elif self.action == "remove_member":
            return AddOrRemoveMemberSerializer
    
    @action(detail=True,methods=['post'])
    def add_member(self,request,pk=None):
        team = self.get_object()
        pass
    @action(detail=True,methods=['post'])
    def remove_member(self,request,pk=None):
        team = self.get_object()
        pass
    