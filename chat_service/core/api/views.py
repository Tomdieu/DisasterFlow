from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,ListModelMixin,UpdateModelMixin,DestroyModelMixin

from rest_framework.viewsets import GenericViewSet

from .serializer import ChatListSerializer,ChatSerializer,ChatUserSerializer,CreateDiscussionChatSerializer,CreateGroupChatSerializer,MessageListSerializer

from core.models import Chat,ChatUser,Message


class CreateDiscussionChatView(CreateModelMixin,GenericViewSet):
    serializer_class = CreateDiscussionChatSerializer
    queryset = Chat.objects.all()


class CreateGroupChatView(CreateModelMixin,GenericViewSet):
    serializer_class = CreateGroupChatSerializer
    queryset = Chat.objects.all()

class ChatListView(ListModelMixin,GenericViewSet):
    serializer_class = ChatListSerializer
    queryset = Chat.objects.all()