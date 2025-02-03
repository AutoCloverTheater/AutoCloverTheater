import threading

import cv2

from src.facades.Emulator.Emulator import ConnectEmulator, UpdateSnapShot, Click, Swipe, GetSnapShot
from src.facades.Logx.Logx import logx


def test_emulator():
    ConnectEmulator()

    def show():
        Swipe((0.5,0.5),(0.1,0.5))
        Swipe((0.5,0.5),(0.9,0.5))
        Swipe((0.5,0.5),(0.5,0.1))
        Swipe((0.5,0.5),(0.5,0.9))
        Click((0.5, 0.5))

    timer = threading.Timer(1, show)
    timer.start()

    while True:
        UpdateSnapShot()
        res = GetSnapShot()
        if res is not None:
            cv2.imshow("sp", res)
        else:
            logx.warning("Snapshot is None, skipping display")

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 按 'q' 退出
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    test_emulator()