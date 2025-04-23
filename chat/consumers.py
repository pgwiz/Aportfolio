# chat/consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Message

User = get_user_model()

class SecureChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # Verify authenticated user
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return

        self.room_group_name = f"user_{user.id}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        message_type = content.get('type')

        if message_type == 'chat_message':
            await self.handle_chat_message(content)
        elif message_type == 'typing_indicator':
            await self.handle_typing_indicator(content)

    async def handle_chat_message(self, content):
        # Validate and save message
        message = content.get('message')
        receiver_id = content.get('receiver_id')

        if not message or not receiver_id:
            return await self.send_json({'error': 'Invalid message format'})

        if len(message) > 1000:
            return await self.send_json({'error': 'Message too long'})

        receiver = await self.get_user(receiver_id)
        if not receiver:
            return await self.send_json({'error': 'Receiver not found'})

        await self.save_message(
            sender=self.scope["user"],
            receiver=receiver,
            content=message
        )

        # Broadcast to receiver
        await self.channel_layer.group_send(
            f"user_{receiver_id}",
            {
                'type': 'chat.message',
                'message': message,
                'sender': self.scope["user"].username,
                'timestamp': str(timezone.now())
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send_json(event)

    async def handle_typing_indicator(self, content):
        receiver_id = content.get('receiver_id')
        is_typing = content.get('is_typing', False)

        if not receiver_id:
            return

        await self.channel_layer.group_send(
            f"user_{receiver_id}",
            {
                'type': 'typing.indicator',
                'sender': self.scope["user"].username,
                'is_typing': is_typing
            }
        )

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, sender, receiver, content):
        Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content
        )

    async def send_stats_update(self, user_id):
        stats = await self.get_portfolio_stats(user_id)
        await self.channel_layer.group_send(
            f"stats_{user_id}",
            {
                "type": "stats.update",
                "data": stats
            }
        )

    @database_sync_to_async
    def get_portfolio_stats(self, user_id):
        from profile_app.models import Profile
        try:
            profile = Profile.objects.get(user__id=user_id)
            return {
                'projects': profile.projects.count(),
                'skills': profile.skills.count()
            }
        except Profile.DoesNotExist:
            return {}
            
# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))            