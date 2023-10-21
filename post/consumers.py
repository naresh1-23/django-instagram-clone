import json
from user.models import User, Profile
from .models import Post,Comment
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async



class CommentConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def save_message(self,comment, post_id, user_id):
        post = Post.objects.filter(id = int(post_id)).first()
        user = User.objects.filter(id = int(user_id)).first()
        profile = Profile.objects.filter(user = user).first()
        comment = Comment.objects.create(comment =comment, post = post, user = user)
        comment.save()
        return profile.profile_img.url, user.username
        
    async def connect(self):
        self.post_id = self.scope["url_route"]["kwargs"]["post_id"]
        self.post_group_name = f"post_{self.post_id}"

        # Join room group
        await self.channel_layer.group_add(self.post_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.post_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        comment = text_data_json["comment"]
        post_id = self.post_id
        user_id = text_data_json["user"]
        profile, user = await self.save_message(comment, post_id, user_id)
        # Send message to room group
        await self.channel_layer.group_send(
            self.post_group_name, {"type": "chat_message", "comment": comment, "user": user, "profile" : profile}
        )

    # Receive message from room group
    async def chat_message(self, event):
        comment = event["comment"]
        user = event["user"]
        profile = event["profile"]
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"comment": comment, "user": user, "profile": profile}))