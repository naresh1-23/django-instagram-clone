from django.urls import re_path

from . import consumers
from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/comment/(?P<post_id>\w+)/$", consumers.CommentConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<room_id>\w+)/$", ChatConsumer.as_asgi()),
]