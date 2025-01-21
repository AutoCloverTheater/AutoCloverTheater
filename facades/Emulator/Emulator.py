import sys
import time

import numpy
from airtest.core.android import Android
from airtest.core.api import connect_device
from facades.Configs.Config import Config
from facades.Emulator import EmulatorFacades
from facades.Logx.Logx import logx
from mac.emulator.bluestacks import Bluestacks
from mac.emulator.mumu import Mumu as MumuMac
from win.emulator.mumu import Mumu as MumuWin

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

    def ConnectDevice(self):
        """
        连接设备并返回设备序列号。

        Returns:
            device instance
        """
        serial = self.instance.searchAndOpenDevice()
        logx.info(f"准备连接设备「Android:///127.0.0.1:{serial}」")
        self.device = connect_device(f"Android:///127.0.0.1:{serial}?cap_method=JAVACAP&touch_method=adb")
        logx.info(f"连接设备成功「Android:///127.0.0.1:{serial}」")
        EmulatorFacades.ActivityEmulator = self
        return self

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

def ConnectEmulator() :
    """
    连接模拟器
    """
    if EmulatorFacades.ActivityEmulator is None:
        ActivityEmulator = Emulator()
        EmulatorFacades.ActivityEmulator = ActivityEmulator.ConnectDevice()


# 公共方法全局使用
def UpdateSnapShot():
    if EmulatorFacades.ActivityEmulator is None:
        ConnectEmulator()
    EmulatorFacades.ActivityEmulator.selfSnapshot()
def GetSnapShot()->numpy.array:
    return EmulatorFacades.ActivityEmulator.selfGetCachedSnapShot()


if __name__ == "__main__":
    ConnectEmulator()
    UpdateSnapShot()
    print(GetSnapShot())