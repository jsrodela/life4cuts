import json
import requests
from main import settings


VIDEO_SERVER_URL = settings.VIDEO_SERVER_URL


def send_post(video_path):
    try:
        files = {'file': open(video_path, 'rb')}
        values = {}

        r = requests.post(VIDEO_SERVER_URL, files=files, data=values)
        response = json.loads(r.content)
        match response['status']:
            case 'success':
                print('Video send complete')
                return response['code']
            case _:
                print('Invalid response from video server;', r.raw)
                return None
    except Exception as ex:
        print("Exception while sending to video server;", ex)
        return None


def pre_code():
    try:
        r = requests.post(VIDEO_SERVER_URL + "/pre_code")
        response = json.loads(r.content)

        match response['status']:
            case 'success':
                code = response['code']
                print('Received code', code)
                return code
            case _:
                print('Invalid response from video server;', r.raw)
                return None
    except Exception as ex:
        print("Exception while sending to video server;", ex)
        return None


def post_file(code: int, video_path):
    try:
        files = {'file': open(video_path, 'rb')}
        values = {'code': code}

        r = requests.post(VIDEO_SERVER_URL + "/post_file", files=files, data=values)
        response = json.loads(r.content)
        match response['status']:
            case 'success':
                print('Video file upload complete')
                return True
            case _:
                print('Invalid response from video server;', r.raw)
                return False
    except Exception as ex:
        print("Exception while sending to video server;", ex)
        return False
