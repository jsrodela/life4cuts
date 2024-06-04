import base64
import json
import threading

import websocket

from main import settings
from utils import printer

print_list = []
run_thread = False
thread = None

IMG_PATH = settings.PRINT_FILE_NAME


def run_print():
    global run_thread, print_list, thread
    run_thread = True
    print("Thread start")

    while len(print_list):
        data = print_list.pop(0)
        print("Printing", data['code'], '; count:', data['cnt'])
        with open(IMG_PATH, mode='wb') as f:
            f.write(base64.b64decode(data['img']))
        printer.print_file(IMG_PATH, data['cnt'])
    run_thread = False
    thread = None


def add_print(data):
    global thread
    print_list.append(data)
    if not run_thread:
        if thread is not None:
            thread.join()
        thread = threading.Thread(target=run_print, daemon=True)
        thread.start()
        print("Thread started")


def on_message(wsapp, msg):
    # print(msg)
    data = json.loads(msg)
    add_print(data)


if __name__ == '__main__':
    try:
        with open('settings.json', encoding='utf-8') as f:
            conf = json.loads(f.read())
    except FileNotFoundError as err:
        print(err)

    while True:
        ws = websocket.WebSocketApp("ws://" + conf['print_server'] + "/ws/print", on_message=on_message)
        print("Socket connected")
        ws.run_forever()
        print("Socket closed! reconnecting...")
