import json
from user.models import User
from .models import Room, Chat
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async



class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def save_message(self,message, room_id, user_from, user_to):
        room  = Room.objects.filter(id = room_id).first()
        user1 = User.objects.filter(username = user_from).first()
        user2 = User.objects.filter(username = user_to).first()
        chat = Chat.objects.create(message = message, room = room, msg_from = user1, msg_to = user2)
        chat.save()
        
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"post_{self.room_id}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        room_id = self.room_id
        user_from = text_data_json["user_from"]
        user_to = text_data_json["user_to"]
        await self.save_message(message, room_id, user_from,user_to)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message, "user_from": user_from, "user_to" : user_to}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        user_from = event["user_from"]
        user_to = event["user_to"]
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "user_from": user_from, "user_to": user_to}))