# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_room_id = self.scope['url_route']['kwargs']['chat_room_id']
        self.chat_room_group_name = f'chat_{self.chat_room_id}'

        # Check if the user is authenticated
        if not self.scope['user'] or not self.scope['user'].is_authenticated:
            await self.close()  # Close the connection if the user is not authenticated
            return

        # Join the chat room group
        await self.channel_layer.group_add(
            self.chat_room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data['message']
        user = self.scope['user']

        if not user.is_authenticated:
            return

        # Get the chat room
        chat_room = await self.get_chat_room(self.chat_room_id)

        # Create a new message in the database
        new_message = await self.create_message(user, chat_room, message_content)

        # Format the sender's name
        sender_name = f"{user.first_name} {user.last_name}".strip() if user.first_name or user.last_name else user.username

        # Send the message to the room group
        await self.channel_layer.group_send(
            self.chat_room_group_name,
            {
                'type': 'chat_message',
                'message': new_message.content,
                'sender': sender_name,
            }
        )

    @database_sync_to_async
    def get_chat_room(self, chat_room_id):
        return ChatRoom.objects.get(id=chat_room_id)

    @database_sync_to_async
    def create_message(self, sender, chat_room, content):
        return Message.objects.create(sender=sender, chat_room=chat_room, content=content)

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))
