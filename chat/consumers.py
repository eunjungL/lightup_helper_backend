import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from chat.models import Message
from lightup.models import UserInfo
from channels.db import database_sync_to_async
from django.http import request, HttpResponse


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = self.scope["user"]
        username = await self.get_name(user)
        message = text_data_json['message']
        room = text_data_json['room']

        await self.save_message(user, room, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    # receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # send message to webSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @sync_to_async
    def save_message(self, username, room, message):
        Message.objects.create(user=username, room=room, content=message).save()

    @database_sync_to_async
    def get_name(self, user):
        return user.user.username
