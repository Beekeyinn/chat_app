import json
import time
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Room, Message
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room, created = await self.get_room(self.scope['url_route']['kwargs']['room_name'])
        print(self.scope['url_route'])
        self.room = room
        self.room_group_name = 'chat_%s' % self.room.name

        # used to join a group (self.room_group_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket from front end
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # gained if AuthMiddlewareStack is used in asgi.py application variable
        user = self.scope['user']
        # create message object from incoming message and user(gained from AuthMiddlewareStack)
        message_obj = await self.create_message(message, user, self.room)
        self.message = {
            'message': message_obj.message,
            'send_at': int(time.mktime(message_obj.created_at.timetuple()))*1000,
            'send_by': message_obj.user.username
        }
        self.user = {
            'id': user.id,
            'name': user.username,
            'email': user.email,
        }

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                # chat_message is the function name and is called automatically
                'type': 'chat_message',
                'message': self.message,
                'user': self.user
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))

    # converts sychronous function to async
    @database_sync_to_async
    def create_message(self, message, user, room):
        """
            provide message object after created
        """
        message_obj = Message.objects.create(
            message=message, user=user, room_name=room)
        message_obj.save()
        return message_obj

    @database_sync_to_async
    def get_room(self, room_name):
        """
            provide the name of the room if exists existed name or if created created one with created as bool (true)
        """
        room, created = Room.objects.get_or_create(name=room_name)
        return room, created
