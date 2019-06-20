import json
import uuid

from channels.generic.websocket import AsyncWebsocketConsumer
from rest_camel.parser import CamelCaseJSONParser
from rest_camel.util import camelize
from rest_framework import status

from apps.broadcaster.actions import Actions
from apps.broadcaster.cache import (
    add_connection,
    remove_connection,
    list_connected
)
from apps.broadcaster.serializers import MessageSerializer
from settings import (
    MAIN_GROUP_NAME,
    ACTION_MESSAGE_ERROR,
    ACTION_HELLO,
    ACTION_CONNECTED
)


class ConnectionConsumer(AsyncWebsocketConsumer, Actions):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.authenticated = False

        self.id = uuid.uuid4().hex
        self.parser = CamelCaseJSONParser()

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(
            MAIN_GROUP_NAME, self.channel_name
        )
        await add_connection(self.id, self.channel_name)

        await self.send_message(ACTION_HELLO, data=self.id)
        await self.send_connected_list()

        await self.channel_layer.group_send(
            MAIN_GROUP_NAME, {
                "type": 'main_connects',
                "data": self.id
            }
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            MAIN_GROUP_NAME, self.channel_name,
        )
        await remove_connection(self.id)
        await self.channel_layer.group_send(
            MAIN_GROUP_NAME, {
                "type": 'main_disconnects',
                "data": self.id
            }
        )

    async def receive(self, text_data=None, bytes_data=None):

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

    async def send_message(self, action, code=None, data=None):
        if code is None:
            code = status.HTTP_200_OK
        response = {
            'action': action,
            'code': code
        }
        if data is not None:
            response['data'] = data
        serializer = MessageSerializer(response)
        try:
            message = camelize(json.dumps(serializer.data))
        except TypeError:
            message = serializer.data
        await self.send(text_data=message)

    async def send_connected_list(self):
        connected = await list_connected()
        await self.send_message(ACTION_CONNECTED, data=json.dumps(connected))

    async def send_error_bad_request(self):
        await self.send_message(
            action=ACTION_MESSAGE_ERROR,
            code=status.HTTP_400_BAD_REQUEST
        )
