import json
import logging
import subprocess
import time
from facades.Configs.Config import Config

class Mumu:
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
                logging.error(e)
                self._openmumu()
                time.sleep(3)
                total += 1

    def _mumuTollInfoAll(self):
        toolPath = Config.get("app", {}).get("emulatorPath", "")
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

            logging.error(f"mumutool cmd({cmd}) err:{error.decode()}")
            return []
        else:
            obj = json.loads(output.decode())
            return obj["return"]["results"]

    def _openmumu(self):
        toolPath = Config.get("app", {}).get("emulatorPath", "")
        cmd = f"open -a {toolPath}/MuMuPlayer && osascript -e 'tell application \"MuMuPlayer\" to minimize'"
        subprocess.Popen(cmd, shell=True)
    def _openDevice(self, index: int) -> bool:
        toolPath = Config.get("app", {}).get("emulatorPath", "")
        cmd = f"{toolPath}/mumutool open {index}"
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            )
        output, error = process.communicate()
        if error.decode() != "":
           logging.error(f"mumutool cmd({cmd}) err:{error.decode()}")
           return False
        else:
            logging.info(f"打开了设备:{index}")
        return True
    def _closeDevice(self, index: int) -> bool:
        toolPath = Config.get("app", {}).get("emulatorPath", "")
        cmd = f"{toolPath}/mumutool close {index}"
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            )
        output, error = process.communicate()
        if error.decode() != "":
           logging.error(f"mumutool cmd({cmd}) err:{error.decode()}")
           return False
        else:
            obj = json.loads(output.decode())
            if obj["return"].get("err", "") != "" and obj['return']["device"]["state"] != "stopped":
                logging.error(f"关闭设备失败:{obj['return'].get('err', '')}, 准备重试")
                time.sleep(0.5)
                self._closeDevice(index)
            logging.info(f"关闭了设备:{index}")
        return True

    def searchAndOpenDevice(self, port) -> str:
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
                            logging.info(f"等待设备：{openedDevices[index].get('name')}启动")
                            time.sleep(1)
                            total += 1
                            logging.info(f"等待设备：启动 等待：{total} 秒")
                            if total > 10:
                                raise Exception(f"设备{openedDevices[index].get('name')}启动失败")
                            continue
                        else:
                            logging.info(f"设备：{openedDevices[index].get('name')} prot:{openedDevices[index].get('adb_port')} 启动成功")
                            break

            openedDevices = self._mumuTollInfoAll()
            if openedDevices[index].get("adb_port", 0) != int(port):
                logging.info(f"设备：{openedDevices[index].get('name')} prot:{openedDevices[index].get('adb_port')},与需求端口{port}不匹配,准备关闭设备")
                self._closeDevice(index)
                time.sleep(0.2)
                continue
            else:
                serial = Config.get("app", {}).get("adb", "") + ":" + port
                break

        return serial