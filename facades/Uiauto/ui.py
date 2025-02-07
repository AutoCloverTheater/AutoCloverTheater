import datetime

import cv2
import uiautomator2 as u2

from facades.Configs.Config import Config


def connect():
    d = u2.connect(f"127.0.0.1:16480")
    return d

u2Device = connect()

def screenshot():
    return u2Device.screenshot(format='opencv')


def appStart():
    u2Device.app_start('com.moefantasy.clover',wait=True, stop=True)


if __name__ == '__main__':
    connect()
    # print(u2Device.info)
    while True:
        res = screenshot()
        cv2.imshow("png", res)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 按 'q' 退出
            break

    cv2.destroyAllWindows()
