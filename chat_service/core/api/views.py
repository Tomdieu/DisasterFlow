from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,ListModelMixin,UpdateModelMixin,DestroyModelMixin

from rest_framework.viewsets import GenericViewSet

from .serializer import ChatListSerializer,ChatSerializer,ChatUserSerializer,CreateDiscussionChatSerializer,CreateGroupChatSerializer,MessageListSerializer

from core.models import Chat,ChatUser,Message,User

from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema


class CreateDiscussionChatView(CreateModelMixin,GenericViewSet):
    serializer_class = CreateDiscussionChatSerializer
    queryset = Chat.objects.all()


class CreateGroupChatView(CreateModelMixin,GenericViewSet):
    serializer_class = CreateGroupChatSerializer
    queryset = Chat.objects.all()

class ChatViewSet(ListModelMixin,GenericViewSet):
    serializer_class = ChatListSerializer
    queryset = Chat.objects.all()

    @swagger_auto_schema(methods=['post'])
    @action(methods=['post'],detail=True)
    def add_member(self,request,pk=None):
        chat = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"user_id":"This field is required"},status=400)
        if not User.objects.filter(id=user_id).exists():
            return Response({"user_id":"User not found"},status=400)
        if ChatUser.objects.filter(chat=chat,user_id=user_id).exists():
            return Response({"user_id":"User already exists"},status=400)
        ChatUser.objects.create(chat=chat,user_id=user_id)
        return Response({"message":"User added successfully"},status=200)



class MessageViewSet(ListModelMixin,CreateModelMixin,GenericViewSet):
    serializer_class = MessageListSerializer
    queryset = Message.objects.all()