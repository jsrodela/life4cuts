# chat/consumers.py
import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

ROOM_GROUP_NAME = 'PRINT_GROUP'
BASE64_STR = 'data:image/png;base64,'


class PrintConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room group
        await self.channel_layer.group_add(ROOM_GROUP_NAME, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(ROOM_GROUP_NAME, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json["message"]
        #
        # # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name, {"type": "chat.message", "message": message}
        # )
        pass

    # Receive message from room group
    async def send_data(self, data):
        # message = event["message"]
        #
        # # Send message to WebSocket
        # await self.send(text_data=json.dumps({"message": message}))
        # print(data['img'])
        await self.send(text_data=data['data'])


def broadcast_photo(b64, cnt, code):
        asyncio.run(get_channel_layer().group_send(ROOM_GROUP_NAME, {
            'type': 'send_data',
            'data': json.dumps({
                'cnt': cnt,
                'code': code,
                'img': b64
            })
        }))

