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
        print("Exception while sending to printer;", ex)
        return None
