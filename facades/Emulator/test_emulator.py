import time

import cv2
from pyscrcpy import Client

from facades.Emulator.Emulator import ConnectEmulator, UpdateSnapShot


def test_emulator():
    res = ConnectEmulator()
    while 1 :
        time.sleep(1)
        UpdateSnapShot()
