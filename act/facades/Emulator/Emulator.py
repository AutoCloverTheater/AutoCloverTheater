import sys
import threading
import time
from typing import Optional

import numpy
import uiautomator2
import uiautomator2 as u2

from act.facades.Configs.Config import Config
from act.facades.Emulator.linux.mumu import Mumu as MumuLinux
from act.facades.Emulator.mac.bluestacks import Bluestacks
from act.facades.Emulator.mac.mumu import Mumu as MumuMac
from act.facades.Emulator.win.mumu import Mumu as MumuWin
from act.facades.Logx.Logx import logx
from act.install_utils import checkAdbutilsBinaries

# 可用的模拟器驱动
UsefulEmulator = {
    "darwin": {
        "mumu": MumuMac,
        "bluestacks": Bluestacks,
    },
    "win32": {
        "mumu": MumuWin,
    },
    "linux":{
        "mumu": MumuLinux,
    }
}

class Emulator:
    instance = MumuMac| MumuWin | Bluestacks | MumuLinux
    device = uiautomator2.Device
    snapshotCache = None

    def __init__(self) -> None:
        """
        初始化 Emulator 类实例。

        Raises:
            Exception: 如果平台或模拟器不支持，则抛出异常。
        """
        self.lock = threading.Lock()

    def ConnectDevice(self):
        """
        连接设备并返回设备序列号。

        Returns:
            device instance
        """
        instance = UsefulEmulator[sys.platform][Config('app').get('emulatorType')]()
        self.instance = instance

        platform = UsefulEmulator.get(sys.platform, None)
        if platform is None:
            raise Exception(f"不支持平台「{platform}」")
        if platform.get(Config("app").get('emulatorType'), None) is None:
            raise Exception(f"平台「{sys.platform}」,不支持模拟器「{Config('app').get('emulatorType')}」")

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
    checkAdbutilsBinaries()
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
    logx.debug(f"点击坐标：{x} ,类型: {type(x).__name__}")
    logx.debug(f"点击坐标：{y} ,类型: {type(y).__name__}")
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

class Pipe:
    def __init__(self) -> None:
        self.breakCondition = False
    def wait(self, fun, retry = 45):
        if self.breakCondition:
            return self

        for i in range(retry):
            UpdateSnapShot()
            res, ok = fun()
            if ok :
                break
            if i == retry - 1:
                self.breakCondition = True

        return self

    def waitThrough(self, fun, retry = 45):
        if self.breakCondition:
            return self

        for i in range(retry):
            UpdateSnapShot()
            res, ok = fun()
            if ok :
                break

        return self

    def waitAndClick(self, fun, retryFps = 45):
        """
        等待并且点击-调用中断
        :param fun:
        :param retryFps:
        :return:
        """
        if self.breakCondition:
            return self

        for i in range(retryFps):
            UpdateSnapShot()
            res, ok = fun()
            if ok :
                Click(res['pot'])
                break
            if i == retryFps - 1:
                self.breakCondition = True

        return self

    def waitAndClickCallback(self, fun, callback,retryFps = 45):
        """
        等待并且点击-调用中断
        点击完成后调用回调函数
        :param fun:
        :param callback:
        :param retryFps:
        :return:
        """
        if self.breakCondition:
            return self

        for i in range(retryFps):
            UpdateSnapShot()
            res, ok = fun()
            if ok :
                Click(res['pot'])
                callback()
                break
            if i == retryFps - 1:
                self.breakCondition = True

        return self

    def waitAndCallback(self, fun, callback,retryFps = 45):
        """
        点击完成后调用回调函数
        :param fun:
        :param callback:
        :param retryFps:
        :return:
        """
        for i in range(retryFps):
            UpdateSnapShot()
            res, ok = fun()
            if ok :
                # Click(res['pot'])
                callback(res)
                break
            if i == retryFps - 1:
                self.breakCondition = True

        return self

    def waitAndClickThrough(self, fun, retryFps = 45):
        """
        等待并且点击-链式调用不中断
        :param fun:
        :param retryFps:
        :return:
        """
        if self.breakCondition:
            return self

        for i in range(retryFps):
            UpdateSnapShot()
            res, ok = fun()
            if ok :
                Click(res['pot'])
                break

        return self

    def waitUntil(self, fun1,fun2, retryFps = 45):
        """
        :param fun1:
        :param fun2:
        :param retryFps:
        :return:
        """
        while retryFps > 0:
            UpdateSnapShot()
            res1, ok1 = fun1()
            if ok1:
                continue
            res2, ok2 = fun2()
            if ok2:
                Click(res2['pot'])
                break
            if not ok1 and not ok2:
                retryFps -= 1
                # raise Exception("未知页面")
        return self

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
