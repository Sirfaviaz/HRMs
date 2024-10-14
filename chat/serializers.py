from rest_framework import serializers
from .models import ChatRoom, Message
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model, used to display user information."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email','first_name', 'last_name']

class ChatRoomSerializer(serializers.ModelSerializer):
    """Serializer for ChatRoom model to handle chat room data."""
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.CharField(read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'participants', 'is_private', 'last_message']

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model to handle chat messages."""
    sender = UserSerializer(read_only=True)
    chat_room = serializers.PrimaryKeyRelatedField(queryset=ChatRoom.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'sender', 'chat_room', 'content', 'timestamp']
