from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/groupchat/(?P<group_name>\w+)/$', consumers.GroupChatConsumer.as_asgi()),
]