from rest_framework.routers import DefaultRouter

from .views import CreateDiscussionChatView,CreateGroupChatView, ChatViewSet,MessageViewSet

router = DefaultRouter()

router.register(r'chats', ChatViewSet, basename='chats')
router.register(r'create-discussion-chat', CreateDiscussionChatView, basename='create-discussion-chat')
router.register(r'create-group-chat', CreateGroupChatView, basename='create-group-chat')
router.register(r'messages', MessageViewSet, basename='messages')