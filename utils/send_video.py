import json
import requests


VIDEO_SERVER_URL = 'https://jamsin.tk/api'


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
        r = requests.post("https://jamsin.tk/pre_code")
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

        r = requests.post("https://jamsin.tk/post_file", files=files, data=values)
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
