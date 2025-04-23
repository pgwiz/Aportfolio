# chat/views.py
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Message, Notification
from .serializers import MessageSerializer, NotificationSerializer
from django.db.models import Q
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework import viewsets

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
class NotificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing notifications.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
# REST API Views
class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('-timestamp')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(receiver=user))

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class MarkNotificationSeenView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        instance.is_seen = True
        instance.save()
        return Response(self.get_serializer(instance).data)

# WebSocket Consumer
class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
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
        message = content['message']
        receiver_id = content['receiver_id']
        
        # Save message and create notification
        message_obj = await self.save_message(
            sender=self.scope["user"],
            receiver_id=receiver_id,
            content=message
        )
        
        # Broadcast to receiver
        await self.channel_layer.group_send(
            f"user_{receiver_id}",
            {
                "type": "chat.message",
                "message": message_obj.content,
                "sender": message_obj.sender.username,
                "timestamp": str(message_obj.timestamp)
            }
        )

    async def chat_message(self, event):
        await self.send_json(event)

    async def handle_typing_indicator(self, content):
        receiver_id = content['receiver_id']
        await self.channel_layer.group_send(
            f"user_{receiver_id}",
            {
                "type": "typing.indicator",
                "sender": self.scope["user"].username,
                "is_typing": content['is_typing']
            }
        )

    @database_sync_to_async
    def save_message(self, sender, receiver_id, content):
        from .models import Message, Notification
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        receiver = User.objects.get(id=receiver_id)
        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content
        )
        Notification.objects.create(
            user=receiver,
            notification_type='message',
            content=f"New message from {sender.username}"
        )
        return message
        
        
from rest_framework.throttling import AnonRateThrottle

class ContactFormView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    throttle_classes = [AnonRateThrottle]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        admin_user = PortfolioUser.objects.get(is_superuser=True)
        serializer.save(
            sender=None,
            receiver=admin_user,
            is_contact_form=True
        )        