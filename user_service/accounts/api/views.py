from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.decorators import action

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from django.contrib.auth import authenticate, login, logout

from rest_framework.authtoken.models import Token

User = get_user_model()

from accounts.models import Citizen, EmergencyResponder, EmergencyResponseTeam, Profile
from .serializers import CitizenSerializer, EmergencyResponderSerializer, EmergencyResponseTeamSerializer, \
    ProfileSerializer, LoginSerializer, UserSerializer, CitizenListSerializer, EmergencyResponderListSerializer, \
    EmergencyResponseTeamListSerializer, MemberSerializer


class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):

        if self.action == 'list':
            return UserSerializer
        elif self.action in ["info"]:
            return UserSerializer
        return UserSerializer

    @action(methods=['get'], detail=False, url_path='user-info')
    def info(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CitizenViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = CitizenSerializer
    queryset = Citizen.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CitizenListSerializer
        elif self.action in ["profile", "update_profile"]:
            return ProfileSerializer
        return CitizenSerializer

    @action(detail=True, methods=['GET'])
    def profile(self, request, pk=None):
        citizen_object = self.get_object()
        profile = citizen_object.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def update_profile(self, request, pk=None):
        citizen_object = self.get_object()
        profile = citizen_object.profile
        serializer = ProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(detail=True, methods=['post'])
    # def set_password(self, request, pk=None):
    #     user = self.get_object()
    #


class EmergencyResponderViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = EmergencyResponderSerializer
    queryset = EmergencyResponder.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return EmergencyResponderListSerializer
        elif self.action in ["profile", "update_profile"]:
            return ProfileSerializer
        elif self.action in ["create_team"]:
            return EmergencyResponseTeamSerializer
        elif self.action in ['add_team_member']:
            return MemberSerializer
        return EmergencyResponderSerializer

    @action(detail=True, methods=['GET'])
    def profile(self, request, pk=None):
        citizen_object = self.get_object()
        profile = citizen_object.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(detail=True, methods=['post'])
    # def set_password(self, request, pk=None):
    #     user = self.get_object()

    @action(detail=True, methods=['get'])
    def teams(self, request):

        object = self.get_object()
        teams = object.team_set.all()
        serializer = EmergencyResponseTeamListSerializer(teams, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def create_team(self, request):
        object = self.get_object()
        serializer = EmergencyResponseTeamSerializer(data=request.data)
        # add the authenticated user to the emergency response team newly created
        if serializer.is_valid(raise_exception=True):
            team = serializer.save()
            team.members.add(object)

            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)

        else:
            return Response({"success": False, "message": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_team_member(self, request):
        object = self.get_object()
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            team = serializer.validated_data["team_id"]
            team.members.add(object)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "message": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


# class EmergencyResponseTeamViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin,
#                                    GenericViewSet):
#     authentication_classes = [TokenAuthentication, SessionAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     queryset = EmergencyResponseTeam.objects.all()
#     serializer_class = EmergencyResponseTeamSerializer


class RegisterEmergencyResponderViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = EmergencyResponderSerializer
    queryset = EmergencyResponder.objects.all()


class RegisterCitizenResponderViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = CitizenSerializer
    queryset = Citizen.objects.all()


class LoginViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)

            token: str = ""

            token_obj, created = Token.objects.get_or_create(user=user)

            return Response({"token": token_obj.key, "success": True, "data": UserSerializer(user)},
                            status=status.HTTP_200_OK)

        return Response({"success": False, "message": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
