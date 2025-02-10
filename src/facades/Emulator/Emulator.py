import sys
import threading
import time
from typing import Optional

import numpy
import uiautomator2

from src.facades.Configs.Config import Config
import uiautomator2 as u2

from src.facades.Emulator.mac.bluestacks import Bluestacks
from src.facades.Emulator.mac.mumu import Mumu as MumuMac
from src.facades.Emulator.win.mumu import Mumu as MumuWin
from src.facades.Logx.Logx import logx

# 可用的模拟器驱动
UsefulEmulator = {
    "darwin": {
        "mumu": MumuMac,
        "bluestacks": Bluestacks,
    },
    "win32": {
        "mumu": MumuWin,
    }
}

class Emulator:
    instance = MumuMac| MumuWin | Bluestacks
    device = uiautomator2.Device
    snapshotCache = None

    def __init__(self) -> None:
        """
        初始化 Emulator 类实例。

        Raises:
            Exception: 如果平台或模拟器不支持，则抛出异常。
        """

        platform = UsefulEmulator.get(sys.platform, None)
        if platform is None:
            raise Exception(f"不支持平台「{platform}」")

        if platform.get(Config("app").get('emulatorType'), None) is None:
            raise Exception(f"平台「{sys.platform}」,不支持模拟器「{Config('app').get('emulatorType')}」")

        instance = UsefulEmulator[sys.platform][Config('app').get('emulatorType')]()
        self.instance = instance

        self.lock = threading.Lock()

    def ConnectDevice(self):
        """
        连接设备并返回设备序列号。

        Returns:
            device instance
        """
        serial = self.instance.getConnectStr()
        logx.info(f"准备连接设备「{serial}」")
        self.device = u2.connect(serial)
        logx.info(f"连接设备成功「{serial}」")

        dpi = int(self.device.info["displayWidth"]/self.device.info["displaySizeDpX"]*160)
        if self.device.info['displayWidth'] != Config('app.displayWidth'):
            logx.exception(f"设备屏幕宽需要设置为{Config('app.displayWidth')}")
            raise Exception(f"设备屏幕宽需要设置为{Config('app.displayWidth')}")
        if self.device.info['displayHeight'] != Config('app.displayHeight'):
            logx.exception(f"设备屏幕高需要设置为{Config('app.displayHeight')}")
            raise Exception(f"设备屏幕高需要设置为{Config('app.displayHeight')}")

        if dpi != Config('app.dpi'):
            logx.exception(f"设备dpi，必须为{Config('app.dpi')}")
            raise Exception(f"设备dpi，必须为{Config('app.dpi')}")


        logx.info(f'设备信息 屏幕宽：{self.device.info["displayWidth"]} 高：{self.device.info["displayHeight"]} dpi：{int(self.device.info["displayWidth"]/self.device.info["displaySizeDpX"]*160)}')
        return self

    def updateSnapShop(self):
        with self.lock:
            self.snapshotCache = self.device.screenshot(format='opencv')
            return self.snapshotCache



    def selfGetCachedSnapShot(self):
        with self.lock:
            return self.snapshotCache

# 已经激活的模拟器
ActivityEmulator = Emulator()

def ConnectEmulator() :
    """
    连接模拟器
    """
    return ActivityEmulator.ConnectDevice()


# 公共方法全局使用
def UpdateSnapShot():
    return ActivityEmulator.updateSnapShop()
def GetSnapShot()->numpy.array:
    img = ActivityEmulator.selfGetCachedSnapShot()
    if img is None:
        return UpdateSnapShot()
    return ActivityEmulator.selfGetCachedSnapShot()


def Click(point:tuple[float|int,float|int], sleep=0.3):
    x,y = point
    if type(x) == float and int(x) <= 1 and int(y) <= 1:
        x = int(x * ActivityEmulator.device.info["displayWidth"])
        y = int(y * ActivityEmulator.device.info["displayHeight"])

    ActivityEmulator.device.click(x, y)
    time.sleep(sleep)

def Text(text:str):
    ActivityEmulator.device.send_keys(text,clear=True)
    time.sleep(0.3)
    return

def Swipe(start:tuple[float|int,float|int], end:tuple[float|int,float|int], steps: Optional[int] = None, sleep=0.1):
    x,y = start
    x1, y1 = end
    if type(x) == float:
        x = int(x * ActivityEmulator.device.info["displayWidth"])
        y = int(y * ActivityEmulator.device.info["displayHeight"])
        x1 = int(x1 * ActivityEmulator.device.info["displayWidth"])
        y1 = int(y1 * ActivityEmulator.device.info["displayHeight"])

    ActivityEmulator.device.swipe(x,y,x1,y1,steps)
    time.sleep(sleep)

def AppCurrent():
    """
    检测四叶草是否已经启动
    """
    resp = ActivityEmulator.device.app_current()
    if resp is not None and resp.get("package") != Config('app.appName'):
        logx.warning(f"应用「{Config('app.appName')}」,未启动")

    return resp.get("package") == Config('app.appName')


def AppStart():
    ActivityEmulator.device.app_start(Config('app.appName'), wait=True)


if __name__ == "__main__":
    ConnectEmulator()
    resp = ActivityEmulator.device.app_current()
    logx.info(f"app_current:{resp}")
    resp = ActivityEmulator.device.app_info(Config("app.appName"))
    logx.info(f"app_info:{resp}")
    resp = ActivityEmulator.device.app_list_running()
    logx.info(f"app_list_running:{resp}")
    resp = ActivityEmulator.device.app_list()
    logx.info(f"app_list:{resp}")

    AppStart()
