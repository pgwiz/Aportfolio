# chat/routing/websocket_urls.py
from django.urls import re_path
from ..consumers import ChatConsumer  # Import from parent directory

websocket_urlpatterns = [
    re_path(r"ws/chat/$", ChatConsumer.as_asgi()),
]