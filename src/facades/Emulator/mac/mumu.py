import json
import subprocess
import time

from src.facades.Configs.Config import Config
from src.facades.Logx.Logx import logx


class Mumu:
    def getConnectStr(self) -> str:
        return f'{Config("app.addr")}:{Config("app.serial")}'

    def getSerial(self)-> list:
        return self._mumuTollInfoAll()

    def getAllSerial(self)-> list:
        total = 0
        while 1:
            try:
                return self._mumuTollInfoAll()
            except Exception as e:
                if total > 3:
                    raise Exception("模拟器启动失败")
                logx.error(e)
                self._openmumu()
                time.sleep(3)
                total += 1
    def mumuInfoAll(self):
        return self._mumuTollInfoAll()
    def _mumuTollInfoAll(self):
        toolPath = Config("app", {}).get("emulatorPath", "")
        cmd = f"{toolPath}/mumutool info all"
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            )
        output, error = process.communicate()
        if error.decode() != "":
            if error.decode() == "Error: invalidPort\n":
                raise Exception("mumu模拟器尚未启动")

            logx.error(f"mumutool cmd({cmd}) err:{error.decode()}")
            return []
        else:
            obj = json.loads(output.decode())
            return obj["return"]["results"]

    def _openmumu(self):
        toolPath = Config("app", {}).get("emulatorPath", "")
        cmd = f"open -a {toolPath}/MuMuPlayer"
        subprocess.Popen(cmd, shell=True)

    def openEmulator(self):
         self._openmumu()

    def openDevice(self, index):
       self._openDevice(index)

    def closeDevice(self, index):
        self._closeDevice(index)

    def _openDevice(self, index: int) -> bool:
        times = 30
        status = True
        while True:
            if times <= 0:
                logx.error(f"打开设备失败:{index}")
                raise Exception(f"打开设备失败:{index}")

            toolPath = Config("app", {}).get("emulatorPath", "")
            cmd = f"{toolPath}/mumutool open {index}"
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                )
            output, error = process.communicate()
            if error.decode() != "":
                times-=1
                time.sleep(1)
                continue
            else:
                break

        times = 30
        status = False
        while True:
            if times <= 0:
                logx.error(f"启动设备失败:{index}")
                raise Exception(f"启动设备失败:{index}")

            # 查看是否已经在运行
            res = self._mumuTollInfoAll()

            for device in res:
                logx.info(device)
                if int(device.get("index")) == index and device.get("state") == "running":
                    logx.info("running")
                    status = True
            if not status:
                times-=1
                time.sleep(1)
                continue
            else:
                break
        logx.info(f"打开了设备:{index}")
        return status
    def _closeDevice(self, index: int) -> bool:
        toolPath = Config("app", {}).get("emulatorPath", "")
        cmd = f"{toolPath}/mumutool close {index}"
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            )
        output, error = process.communicate()
        if error.decode() != "":
           logx.error(f"mumutool cmd({cmd}) err:{error.decode()}")
           return False
        else:
            obj = json.loads(output.decode())
            if obj["return"].get("err", "") != "" and obj['return']["device"]["state"] != "stopped":
                logx.error(f"关闭设备失败:{obj['return'].get('err', '')}, 准备重试")
                time.sleep(0.5)
                self._closeDevice(index)
            logx.info(f"关闭了设备:{index}")
        return True

    def searchAndOpenDevice(self) -> str:
        devices = self._mumuTollInfoAll()
        if len(devices) == 0:
            self._openmumu()
            time.sleep(3)
            devices = self._mumuTollInfoAll()

        openIndex = Config("app", {}).get("serial")
        prot = ""
        for index, device in enumerate(devices) :
            if index == int(openIndex):
                if device.get("state") == "running":
                    prot = device.get('adb_port')
                    break
                if device.get("state") != "running":
                    self._openDevice(index)
                    ## 等待设备启动
                    total = 0
                    while 1:
                        openedDevices = self._mumuTollInfoAll()
                        if openedDevices[index].get("adb_port", 0) == 0:
                            logx.info(f"等待设备：{openedDevices[index].get('name')}启动")
                            time.sleep(1)
                            total += 1
                            logx.info(f"等待设备：启动 等待：{total} 秒")
                            if total > 10:
                                raise Exception(f"设备{openedDevices[index].get('name')}启动失败")
                            continue
                        else:
                            logx.info(
                                f"设备：{openedDevices[index].get('name')} prot:{openedDevices[index].get('adb_port')} 启动成功")
                            port = openedDevices[index].get("adb_port")
                            break
            else: print(f"设备：{device.get('name')} 状态：{device.get('state')}")

        if prot != "":
            return f"{Config('app.addr')}:{prot}"

        raise Exception(f"没有找到设备 index of {openIndex}")

    def _searchAndOpenDevice(self, port) -> str:
        """
        搜索并且打开模拟器
        ⚠️：mumu最好是通过索引来打开设备
        :param port:
        :return:
        """
        serial = ""
        devices = self._mumuTollInfoAll()
        if len(devices) == 0:
            self._openmumu()
            time.sleep(3)
            devices = self._mumuTollInfoAll()
        # 循环开启模拟器，判断端口
        for index, device in enumerate(devices) :
            if device.get("state") != "running" and device.get("adb_port", "") != port:
                    self._openDevice(index)
                    ## 等待设备启动
                    total = 0
                    while 1:
                        openedDevices = self._mumuTollInfoAll()
                        if openedDevices[index].get("adb_port", 0) == 0:
                            logx.info(f"等待设备：{openedDevices[index].get('name')}启动")
                            time.sleep(1)
                            total += 1
                            logx.info(f"等待设备：启动 等待：{total} 秒")
                            if total > 10:
                                raise Exception(f"设备{openedDevices[index].get('name')}启动失败")
                            continue
                        else:
                            logx.info(f"设备：{openedDevices[index].get('name')} prot:{openedDevices[index].get('adb_port')} 启动成功")
                            break

            openedDevices = self._mumuTollInfoAll()
            if openedDevices[index].get("adb_port", 0) != int(port):
                logx.info(f"设备：{openedDevices[index].get('name')} prot:{openedDevices[index].get('adb_port')},与需求端口{port}不匹配,准备关闭设备")
                self._closeDevice(index)
                time.sleep(0.2)
                continue
            else:
                serial = Config("app", {}).get("adb", "") + ":" + port
                break

        return serial