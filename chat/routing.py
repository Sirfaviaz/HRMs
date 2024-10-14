from django.urls import re_path
from .consumers import ChatConsumer  # Import the ChatConsumer class directly

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_room_id>\w+)/$', ChatConsumer.as_asgi()),
]