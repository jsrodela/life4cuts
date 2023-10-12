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

from main import settings
from main.settings import STORAGE
from utils.combine_photo import combine_photo
from . import models

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from utils import webcam, chroma, make_video, send_video, send_print

CAM_GROUP_NAME = 'WEBCAM_GROUP'
LOADING_GROUP_NAME = 'LOADING_GROUP'
BASE64_STR = 'data:image/png;base64,'

do_capture = False


class CamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room group
        await self.channel_layer.group_add(CAM_GROUP_NAME, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(CAM_GROUP_NAME, self.channel_name)

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
        data = json.loads(text_data)
        match data['type']:
            case 'cap':
                do_capture = data['num']
            case 'end':
                start_loading_thread()
                await self.send('end')
                end_thread()
            case _:
                print('Unknown received data;', data)
        pass

    # Receive message from room group
    async def send_data(self, data):
        # message = event["message"]
        #
        # # Send message to WebSocket
        # await self.send(text_data=json.dumps({"message": message}))
        # print(data['img'])
        await self.send(text_data=data['data'])


def cam_send(data: str):
    asyncio.run(get_channel_layer().group_send(CAM_GROUP_NAME, {
        'type': 'send_data',
        'data': data
    }))


def cam_while():
    global do_capture, run_thread
    # now = datetime.now()

    while run_thread:
        data = webcam.getFrame()
        b64 = data.decode('utf-8')
        cam_send(b64)

        if do_capture:
            # start_photo_thread(data, do_capture)
            manage_photo(data, do_capture)
            do_capture = 0
            cam_send('resume')

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

    photo_corrected = chroma.correct_photo(photo, settings.conf['chroma'], models.bg_path(models.cut.bg))
    print("Corrected Photo", order)

    chroma_photo = models.cut.add_chroma(photo_corrected, order)
    print("Saved Photo Chroma", order)


latest_loading = {
    "type": "send_data",
    "data": json.dumps({
        "percent": 0,
        "status": "마무리 중",
        "tip": "이제 마지막 단계만 남았어요!"
    })
}


def clear_loading():
    global latest_loading
    latest_loading = {
        "type": "send_data",
        "data": json.dumps({
            "percent": 0,
            "status": "마무리 중",
            "tip": "이제 마지막 단계만 남았어요!"
        })
    }


class LoadingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(LOADING_GROUP_NAME, self.channel_name)
        await self.accept()
        await self.send_data(latest_loading)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(LOADING_GROUP_NAME, self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_data(self, data):
        global latest_loading
        latest_loading = data
        await self.send(text_data=data['data'])


def loading_update(order: int, status: str, tip: str):
    asyncio.run(get_channel_layer().group_send(LOADING_GROUP_NAME, {
        'type': 'send_data',
        'data': json.dumps({
            'percent': order * 100 // 6,
            'status': status,
            'tip': tip
        })
    }))


loading_thread = None


def start_loading_thread():
    global loading_thread
    loading_thread = threading.Thread(target=manage_loading,
                                      args=[],
                                      daemon=True)
    loading_thread.start()


def manage_loading():
    video_path = str(models.cut.storage() / '잠신네컷.mp4')

    # wait for chroma
    loading_update(1, "사진 보정 중", "방금 찍은 사진을 더 아름답게 꾸미고 있어요.")
    while len(models.cut.chromas) < 6:
        pass

    # make video
    loading_update(2, "동영상 만드는 중", "잠신네컷 찍던 소중한 추억을 배속 영상으로 남겨드려요.")
    make_video.make_video(video_path)

    # send video to jamsin.tk
    loading_update(3, "동영상 올리는 중", "잠신고 파일 공유 서비스인 jamsin.tk에서 다운받을 수 있어요.")
    code = send_video.send_post(video_path)
    if code is None:
        print('Received code None')
    else:
        print('Received code:', code)
        models.cut.video_code = code
        models.cut.save()

    # combine photo
    loading_update(4, "잠신네컷 생성 중", "방금 찍은 6개의 사진을 합치고 있어요.")
    frame_path = "clientapp/static/images/2x3_" + models.cut.frame + ".png"
    result_path = str(models.cut.storage() / "result.png")
    combine_photo(frame_path, models.cut.chromas, result_path, models.cut.video_code)

    # send to printer
    loading_update(5, "출력 준비 중", "1장을 출력하기까지 약 1분 정도 걸려요. 대신 출력 비용은 무료에요!")
    send_print.send_post('http://' + settings.conf['print_server'] + '/send_print', result_path, models.cut.paper_count,
                         models.cut.video_code)

    loading_update(6, "출력 준비 완료!", "by RoDeLa 6.0 ♥")
