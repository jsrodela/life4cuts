import base64
import json

import requests


def send_post(url: str, img_path, cnt: int, code: int) -> bool:
    try:
        with open(img_path, 'rb') as f:
            img = base64.b64encode(f.read()).decode('utf-8')
        # files = {'img': open(img_path, 'rb')}
        values = {'img': img, 'cnt': cnt, 'code': code}

        r = requests.post(url, data=values)
        response = json.loads(r.content)
        match response['status']:
            case 'success':
                print('Printer send complete')
                return True
            case 'error':
                print('Error response from printer:', response['error'])
                return False
            case _:
                print('Invalid response from printer:', r.raw)
                return False
    except Exception as ex:
        print("Exception while sending to printer;", ex)
        return False
