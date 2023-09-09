# chat/consumers.py
import asyncio
import base64
import json
import random
import threading
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from clientapp import static
from utils import webcam

ROOM_GROUP_NAME = 'WEBCAM_GROUP'

do_capture = False
photo_count = 1


class CamConsumer(AsyncWebsocketConsumer):
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
        global do_capture
        do_capture = True
        pass

    # Receive message from room group
    async def send_data(self, data):
        # message = event["message"]
        #
        # # Send message to WebSocket
        # await self.send(text_data=json.dumps({"message": message}))
        # print(data['img'])
        await self.send(text_data=data['img'])

def cam_while():
    global do_capture, photo_count
    now = datetime.now()
    name = str(now.hour) + str(now.minute) + str(now.second)
    static.code = name
    while True:
        data = webcam.getFrame()
        b64 = data.decode('utf-8')
        if do_capture:
            with open('img_' + name + '_' + str(photo_count) + '.png', 'wb') as f:
                f.write(base64.decodebytes(data))
                static.pics.append(f.name)
            do_capture = False

            photo_count += 1
            if photo_count > 6:
                asyncio.run(get_channel_layer().group_send(ROOM_GROUP_NAME, {
                    'type': 'send_data',
                    'img': 'end'
                }))
                photo_count = 1
            # static.pics.append(b64)

        # print(data)
        asyncio.run(get_channel_layer().group_send(ROOM_GROUP_NAME, {
           'type': 'send_data',
           'img': b64
        }))


thread = None
run_thread = False
def start_thread():
    global thread, run_thread
    run_thread = True
    thread = threading.Thread(target=cam_while, daemon=True).start()


def end_thread():
    global run_thread
    run_thread = False