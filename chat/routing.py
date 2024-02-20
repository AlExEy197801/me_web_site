from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/main_chat/secret/bolshoj/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]
