# 已经激活的模拟器
import os
import sys

import cv2
from airtest.core.android import adb
from pyscrcpy import Client

ActivityEmulator = None

def on_frame(client, frame):
    client.control.text("123")
    cv2.imshow('Video', frame)
    cv2.waitKey(1)

if __name__ == '__main__':
    platforms = sys.platform

    package_path = os.path.dirname(adb.__file__)

    tpath = ''
    if platforms == 'win32':
        tpath = f"{package_path}/static/adb/windows/adb.exe"
    elif platforms == 'darwin':
        tpath = f"{package_path}/static/adb/mac/adb"

    os.environ['ADBUTILS_ADB_PATH'] = f'{tpath}'

    client = Client(device='127.0.0.1:16416',max_fps=30, max_size=1280)
    client.start(threaded=True)  # create a new thread for scrcpy
    while 1:
        if client.last_frame is None:
            continue
        on_frame(client, client.last_frame)