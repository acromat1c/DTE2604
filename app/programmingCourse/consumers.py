import json
import re
# from channels.generic.websocket import AsyncWebsocketConsumer
# from django.utils.timezone import now
# from .models import Group, GroupMessage
# from django.contrib.auth import get_user_model
# from channels.db import database_sync_to_async

# User = get_user_model()
#
# class GroupChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.group_name = self.scope['url_route']['kwargs']['group_name']
#         safe_group_name = re.sub(r'[^a-zA-Z0-9\-.]', '_', self.group_name)
#         self.room_group_name = f'chat_{safe_group_name}'
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
#
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']
#         username = data['username']
#
#         # Lagre meldingen i databasen
#         user = await self.get_user(username)
#         group = await self.get_group(self.group_name)
#         msg = await self.create_message(group, user, message)
#         timestamp = msg.created_at.strftime('%Y-%m-%d %H:%M')
#
#         await self.channel_layer.group_send(
#             self.room_group_name,
#         {
#             'type': 'chat_message',
#             'message': message,
#             'username': username,
#             'timestamp': timestamp,
#         }
#     )
#
#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'username': event['username'],
#             'timestamp': event['timestamp'],
#         }))
#
#     @database_sync_to_async
#     def get_user(self, username):
#         return User.objects.get(username=username)
#
#     @database_sync_to_async
#     def get_group(self, name):
#         return Group.objects.get(groupName=name)
#
#     @database_sync_to_async
#     def create_message(self, group, user, content):
#         return GroupMessage.objects.create(group=group, user=user, message=content)
