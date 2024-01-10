from rest_framework import serializers

from core.models import User,ChatUser,Chat,Message

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class ChatUserSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = ChatUser
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'

class MessageListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'

class ChatListSerializer(serializers.ModelSerializer):

    members = UserSerializer(many=True)
    messages = MessageListSerializer(many=True)

    class Meta:

        model = Chat
        fields = '__all__'


class CreateDiscussionChatSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    class Meta:
        fields = ['user_id']

    def validate_user_id(self,value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User not found")
        return value

class CreateGroupChatSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Chat
        fields = ['name','is_group']

