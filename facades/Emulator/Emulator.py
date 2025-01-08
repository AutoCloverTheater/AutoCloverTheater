import sys
import time

import numpy
from airtest.core.android import Android
from airtest.core.api import connect_device
from facades.Configs.Config import Config
from facades.Emulator import EmulatorFacades
from facades.Logx import Logx
from mac.emulator.bluestacks import Bluestacks
from mac.emulator.mumu import Mumu

# 可用的模拟器驱动
UsefulEmulator = {
    "darwin": {
        "mumu": Mumu,
        "bluestacks": Bluestacks,
    },
    "win32": {}
}

class Emulator:
    instance = Mumu | Bluestacks
    device = Android
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

    def ConnectDevice(self) -> str:
        """
        连接设备并返回设备序列号。

        Returns:
            device instance
        """
        serial = self.instance.searchAndOpenDevice()
        Logx.info(f"准备连接设备「Android:///127.0.0.1:{serial}」")
        self.device = connect_device(f"Android:///127.0.0.1:{serial}")
        Logx.info(f"连接设备成功「Android:///127.0.0.1:{serial}」")
        return self.device

    def selfGetCachedSnapShot(self):
        return Snapshot(self.snapshotCache)

    def selfSnapshot(self):
        self.snapshotCache = self.device.snapshot(quality=99)

        count = 0
        while self.snapshotCache is None:
            self.snapshotCache = self.device.snapshot(quality=99)
            count += 1
            if count > 10:
                raise Exception("获取截图失败")
            time.sleep(0.1)

        return Snapshot(self.snapshotCache)

class Snapshot:
    img = None

    def __init__(self, img):
        self.img = img

    def toNpArray(self) -> numpy.array:
        return numpy.array(self.img)

def ConnectEmulator() -> str:
    """
    连接模拟器
    """
    ActivityEmulator = Emulator()
    return ActivityEmulator.ConnectDevice()

# 公共方法全局使用
def UpdateSnapShot():
    EmulatorFacades.ActivityEmulator.selfSnapshot()
def GetSnapShot()->numpy.array:
    return EmulatorFacades.ActivityEmulator.selfGetCachedSnapShot()