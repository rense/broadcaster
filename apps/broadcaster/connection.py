import json

from channels.generic.websocket import AsyncWebsocketConsumer
from rest_camel.parser import CamelCaseJSONParser
from rest_camel.util import camelize
from rest_framework import status

from apps.broadcaster.actions import Actions
from apps.broadcaster.serializers import MessageSerializer
from settings import (
    MAIN_GROUP_NAME
)


class ConnectionConsumer(AsyncWebsocketConsumer, Actions):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.authenticated = False

        self.player = None
        self.parser = CamelCaseJSONParser()

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(
            MAIN_GROUP_NAME, self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        try:
            text_data = json.loads(text_data)
        except ValueError:
            return await self.send_error_bad_request()

        serializer = MessageSerializer(data=text_data)
        if not serializer.is_valid():
            return await self.send_error_bad_request()

        await self.channel_layer.group_send(
            MAIN_GROUP_NAME, {
                "type": 'main_message',
                "data": serializer.validated_data['data']
            }
        )

    async def send_error_bad_request(self):
        await self.send_message(
            code=status.HTTP_400_BAD_REQUEST
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            MAIN_GROUP_NAME, self.channel_name,
        )

    async def send_message(self, code=None, data=None):
        if code is None:
            code = status.HTTP_200_OK
        response = {'code': code}
        if data is not None:
            response['data'] = data
        serializer = MessageSerializer(response)
        try:
            message = camelize(json.dumps(serializer.data))
        except TypeError:
            message = serializer.data
        await self.send(text_data=message)
