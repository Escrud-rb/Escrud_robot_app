# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login, logout, get_user
from django.contrib.auth import authenticate
from asgiref.sync import sync_to_async

#   Import applicaions view
from .ws_robot import robot_views

APP_VIEWS = [
    robot_views(),
]


class MainConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.client = self.scope['url_route']['kwargs']['client']
        self.room_group_name = 'chat'
        self.user = self.scope["user"]
        self.personal = None
        self.organisation_profile = None
        self.hospital_profile = None
        self.pharmacy_profile = None
        self.patient_profile = None
        self.current_profile = None

        print(self.user)

        await self.accept()

        await self.channel_layer.group_add(
            str(self.client),
            self.channel_name
        )

        await self.call_apps(run='connect')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            str(self.client),
            self.channel_name
        )
        await self.call_apps(run='disconnect')

    # Receive message from WebSocket

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        await self.call_apps(data, call_one_app=True)

    async def transfert(self, event):
        print('transfert')
        await self.send(text_data=json.dumps(event['data']))

    async def call_apps(self, data={}, run='main', call_one_app=False):
        for view in APP_VIEWS:
            if run in view:
                if run == 'connect' or run == 'disconnect':
                    await view[run](self)
                    if call_one_app:
                        break
                elif run == 'main' and data['type'] in view['DATA_TYPES']:
                    await view[run](self, data)
                    if call_one_app:
                        break
                else:
                    continue
