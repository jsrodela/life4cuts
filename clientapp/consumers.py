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

# Redis settings
CAM_GROUP_NAME = 'WEBCAM_GROUP'
LOADING_GROUP_NAME = 'LOADING_GROUP'

# Base64 encoding prefix string
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

                start_video_thread(models.cut.video_code)
                await self.send('end')
                end_cam_thread()
            case _:
                print('Unknown received data;', data)
        pass

    # Receive message from room group (Redis -> Client)
    async def send_data(self, data):
        # message = event["message"]
        #
        # # Send message to WebSocket
        # await self.send(text_data=json.dumps({"message": message}))
        # print(data['img'])
        await self.send(text_data=data['data'])


# Send cam data to Redis
def cam_send(data: str):
    asyncio.run(get_channel_layer().group_send(CAM_GROUP_NAME, {
        'type': 'send_data',
        'data': data
    }))


def cam_while():
    global do_capture, run_cam_thread
    # now = datetime.now()

    while run_cam_thread:
        data = webcam.getFrame()
        b64 = data.decode('utf-8')
        cam_send(b64)

        if do_capture:
            # start_photo_thread(data, do_capture)
            manage_photo(data, do_capture)
            do_capture = 0
            cam_send('resume')

    webcam.cleanup()


cam_thread = None
run_cam_thread = False


def start_cam_thread():
    global cam_thread, run_cam_thread
    run_cam_thread = True
    cam_thread = threading.Thread(target=cam_while, daemon=True).start()


def end_cam_thread():
    global cam_thread, run_cam_thread
    run_cam_thread = False
    if cam_thread is not None:
        cam_thread.join()
    cam_thread = None


# Disabled
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

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(LOADING_GROUP_NAME, self.channel_name)

    async def receive(self, text_data):
        await self.send_data(latest_loading)
        pass

    async def send_data(self, data):
        global latest_loading
        latest_loading = data
        await self.send(text_data=data['data'])


def loading_update(order: int, status: str, tip: str):
    asyncio.run(get_channel_layer().group_send(LOADING_GROUP_NAME, {
        'type': 'send_data',
        'data': json.dumps({
            'percent': order * 100 // 4,
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
    # wait for chroma
    loading_update(1, "사진 보정 중", "방금 찍은 사진을 더 아름답게 꾸미고 있어요.")
    while len(models.cut.chromas) < 6:
        pass

    # combine photo
    loading_update(2, "잠신네컷 생성 중", "jamsin.tk에서 영상도 받을 수 있어요.")
    frame_path = "clientapp/static/images/2x3_" + models.cut.frame + ".png"
    result_path = str(models.cut.storage() / "result.png")
    combine_photo(frame_path, models.cut.chromas, result_path, models.cut.video_code)

    # send to printer
    loading_update(3, "출력 준비 중", "출력 비용은 무료에요!")
    send_print.send_post('http://' + settings.conf['print_server'] + '/send_print', result_path, models.cut.paper_count,
                         models.cut.video_code)

    loading_update(4, "출력 준비 완료!", "by RoDeLa 6.0 ♥")


video_thread = None


def start_video_thread(code: int):  # 작업 도중 다음컷 시작할수도 있으므로 매개변수로 따로 가져오기
    global video_thread
    video_thread = threading.Thread(target=manage_video,
                                    args=[code],
                                    daemon=True)
    video_thread.start()


def manage_video(code: int):
    video_path = str(models.cut.storage() / '잠신네컷.mp4')

    # make video
    # loading_update(2, "동영상 만드는 중", "잠신네컷 찍던 소중한 추억을 배속 영상으로 남겨드려요.")
    make_video.make_video(video_path)

    # send video to jamsin.tk
    # loading_update(3, "동영상 올리는 중", "잠신고 파일 공유 서비스인 jamsin.tk에서 다운받을 수 있어요.")
    send_video.post_file(code, video_path)
    print("Video Thread Complete, code:", code)


code_thread = None


def start_code_thread():
    global code_thread
    code_thread = threading.Thread(target=manage_code,
                                   args=[],
                                   daemon=True)
    code_thread.start()


def manage_code():
    # video code
    code = send_video.pre_code()
    if code is None:
        print("Received code None")
    else:
        print("Received code", code)
        models.cut.video_code = code
        models.cut.save()
