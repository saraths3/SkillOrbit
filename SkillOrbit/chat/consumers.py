import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone

from .models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope.get("user")
        if not self.user or not self.user.is_authenticated:
            await self.close()
            return
        self.target_user_id = self.scope["url_route"]["kwargs"]["room_name"]
        user_ids = sorted([str(self.user.id), str(self.target_user_id)])
        self.room_group_name = f"chat_{user_ids[0]}_{user_ids[1]}"
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(self.room_group_name,self.channel_name)
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get("message", "").strip()
        if not message_text:
            return
        msg_obj = await self.save_message(self.target_user_id, message_text)
        formatted_time = msg_obj.created_at.strftime("%I:%M %p") if msg_obj else timezone.now().strftime("%I:%M %p")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_text,
                "sender_id": str(self.user.id),
                "sender_username": self.user.username,
                "created_at": formatted_time
            }
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({
                "message": event["message"],
                "sender_id": event["sender_id"],
                "sender_username": event["sender_username"],
                "created_at": event["created_at"]
            })
        )

    @database_sync_to_async
    def save_message(self, target_user_id, message_text):
        User = get_user_model()
        try:
            target_user = User.objects.get(id=target_user_id)
        except User.DoesNotExist:
            return None
        conversation = Conversation.objects.filter(
            Q(user_one=self.user, user_two=target_user) |
            Q(user_one=target_user, user_two=self.user)
        ).first()
        if conversation is None:
            conversation = Conversation.objects.create(
                user_one=self.user,
                user_two=target_user
            )
        return Message.objects.create(
            conversation=conversation,
            sender=self.user,
            message=message_text
        )