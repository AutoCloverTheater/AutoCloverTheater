import datetime

import uiautomator2 as u2

from facades.Configs.Config import Config


def connect():
    d = u2.connect(f"127.0.0.1:16384")
    return d

u2Device = connect()

def screenshot():
    return u2Device.screenshot(format='opencv')


def appStart():
    u2Device.app_start('com.moefantasy.clover',wait=True, stop=True)


if __name__ == '__main__':
    connect()
    while 1:
        screenshot()
        r = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(r)