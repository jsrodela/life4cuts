# chat/consumers.py
import asyncio
import base64
import json
import random
import threading
from datetime import datetime
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from . import models

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from clientapp import static
from utils import webcam, chroma

ROOM_GROUP_NAME = 'WEBCAM_GROUP'
BASE64_STR = 'data:image/png;base64,'

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
    global do_capture, photo_count, run_thread
    now = datetime.now()
    name = str(now.hour) + str(now.minute) + str(now.second)
    static.code = name

    while run_thread:
        data = webcam.getFrame()
        b64 = data.decode('utf-8')
        if do_capture:
            start_photo_thread(data, photo_count)
            do_capture = False

            photo_count += 1
            if photo_count > 6:
                asyncio.run(get_channel_layer().group_send(ROOM_GROUP_NAME, {
                    'type': 'send_data',
                    'img': 'end'
                }))
                photo_count = 1
                break
            # static.pics.append(b64)

        # print(data)
        asyncio.run(get_channel_layer().group_send(ROOM_GROUP_NAME, {
            'type': 'send_data',
            'img': b64
        }))

    webcam.cleanup()


thread = None
run_thread = False


def start_thread():
    global thread, run_thread
    run_thread = True
    thread = threading.Thread(target=cam_while, daemon=True).start()


def end_thread():
    global thread, run_thread
    run_thread = False
    if thread is not None:
        thread.join()
    thread = None


def start_photo_thread(data, order):
    threading.Thread(target=manage_photo, args=(data, order), daemon=True).start()


def manage_photo(data, order):
    photo = models.cut.add_photo(data, order)
    print("Saved Photo", order)

    photo_corrected = chroma.remove_green_background(photo, models.bg_path(models.cut.bg))
    print("Corrected Photo", order)

    chroma_photo = models.cut.add_chroma(photo_corrected, order)
    print("Saved Photo Chroma", order)
