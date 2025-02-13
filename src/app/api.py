import os.path
import sys
import threading
import time
from pathlib import Path

from flask import request, Blueprint, Response, stream_with_context

from src.config.app import get_config
from src.facades.App.App import data_queue, send_event, clients_lock, clients, timer_executed, getExecuted, setExecuted
from src.facades.Configs.Config import Config
from src.facades.Constant.Constant import ROOT_PATH
from src.facades.Emulator.Emulator import ActivityEmulator, ConnectEmulator
from src.facades.Env.Env import EnvDriver
from src.facades.QueueSchedule.QueueSchedule import taskQueue
from src.facades.Runner.ItemCollectionRunner import inTopLeverItemCollection, beforeTopLeverItemCollection
from src.facades.Runner.RefineryRunner import BeforeRefinery, InRefinery
from src.facades.Runner.guildRunner import beforeInGuild, donate, getReward
from src.facades.Runner.layout.AdventureRunner import FindAdventure
from src.facades.Runner.layout.Back import backMain
from src.facades.Runner.layout.LoginRunner import Login


def generate(client_id):
    try:
        while True:
            send_event.wait(0.1)  # 等待事件触发
            send_event.clear()  # 清除事件

            if data_queue:
                data = data_queue.pop(0)
                setExecuted(True)
                yield f"data: {data} \n\n"
            else:
                yield ""
    except GeneratorExit:
        print("生成器退出：客户端断开连接")
    except Exception as e:
        print(f"发生异常：{str(e)}")

# 创建一个蓝图对象
sse_bp = Blueprint('sse', "sse")
@sse_bp.route('/stream')
def stream():
    client_id = id(Response())

    @stream_with_context
    def ge():
        return generate(client_id)

    response = Response(ge(), mimetype='text/event-stream',headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        })

    with clients_lock:
        clients[client_id] = response
    return response


# 创建一个蓝图对象
api_bp = Blueprint('api', __name__)

@api_bp.route('/trigger', methods=['POST'])
def trigger():
    data = f"data: 1223\n\n"
    with clients_lock:
        data_queue.append(data)
    send_event.set()
    return "Data sent!"

@api_bp.route('/', methods=['GET'])
def index():
    file_path = Path("./src/app/webui/index.html")  # 替换为你的文件路径

    content = file_path.read_text(encoding="utf-8")  # 读取文本文件
    return content,200

@api_bp.route('/api/setting', methods=['GET'])
def getBaseSetting():
    """
    获取模拟器设置
    :return:
    """
    config = get_config()
    config['platform'] = sys.platform

    payload = {
        "itemCollectionTopLever": {  # 高难度每日，打完为止
            "payload": [
                {
                    "label": "绝境战I",
                    "value": "绝境战I"
                }, {
                    "label": "绝境战II",
                    "value": "绝境战II"
                }, {
                    "label": "绝境战III",
                    "value": "绝境战III"
                }, {
                    "label": "绝境战IV",
                    "value": "绝境战IV"
                }
            ]
        },
        "relic": {
            "leverPayload": [{
                "label": "普通难度",
                "value": "普通难度"
            }, {
                "label": "噩梦难度",
                "value": "噩梦难度"
            }],
            "mapPayload": [
                {
                    "label": "沙漠星城",
                    "value": "沙漠星城"
                }, {
                    "label": "热沙寒落",
                    "value": "热沙寒落"
                },
            ]
        },
        "worldTree": {  # 世界树
            "payload": [{
                "label": "死境",
                "value": "死境"
            }]
        }
    }

    config['itemCollectionTopLever']['payload'] = payload['itemCollectionTopLever']['payload']
    config['relic']['leverPayload'] = payload['relic']['leverPayload']
    config['relic']['mapPayload'] = payload['relic']['mapPayload']
    config['worldTree']['payload'] = payload['worldTree']['payload']

    return config,200
@api_bp.route('/api/setting', methods=['POST'])
def saveBaseSetting():
    """
    保存模拟器设置
    :return:
    """
    data = request.get_json()
    envx = EnvDriver().iniFromFile(ROOT_PATH.joinpath("env.yaml"))

    for key, value in data.items():
            envx.setValue(key.upper(), value)
    envx.saveToFile(ROOT_PATH.joinpath("env.yaml"))
    return {
        "code":0,
        "msg":"success",
    }

@api_bp.route('/api/mumuInfoList', methods=['GET'])
def mumuInfoList():
    """
    获取mumu设备列表
    :return:
    """
    ActivityEmulator.instance.openEmulator()
    times = 30
    res = []
    error = None
    while True:
        if times <= 0:
            break

        try:
            res = ActivityEmulator.instance.mumuInfoAll()
            break
        except Exception as e:
            error = e
            times -= 1
            time.sleep(1)
            continue

    if error is None:
        return {
            "code": 0,
            "msg": "success",
            "data": res
        }
    else:
        return {
            "code":500,
            "msg":f"{error}",
        }
@api_bp.route('/api/getEmulatorInstallPath', methods=['GET'])
def getEmulatorInstallPath():
    """
    尝试获取模拟器安装地址
    :return:
    """
    ok = False
    path = "/Applications/MuMuPlayer.app/Contents/MacOS"
    if os.path.exists(path):
        ok = True
    if os.path.exists(f"~/{path}"):
        path = f"~/{path}"
        ok = True

    if ok :
        return {
            "code":0,
            "msg":"success",
            "data":path
        }
    else:
        return {
            "code":500,
            "msg":"未找到模拟器安装路径"
        },400
@api_bp.route('/api/startEmulator', methods=['POST'])
def startEmulator():
    """
    启动模拟器
    :return:
    """
    data = request.get_json()

    ActivityEmulator.instance.openDevice(data['index'])
    return {
        "code":0,
        "msg":"success"
    }
@api_bp.route('/api/stopEmulator', methods=['POST'])
def stopEmulatorReq():
    data = request.get_json()
    ActivityEmulator.instance.closeDevice(data['index'])
    return {
        "code":0,
        "msg":"success"
    }

@api_bp.route('/api/startRun', methods=['POST'])
def startRun():
    """
    开始任务
    :return:
    """
    # 1 读取配置开始编排任务
    # - 高难度每日
    # - 矿厂每日
    # - 世界树
    taskQueue.push(ConnectEmulator)
    taskQueue.push(Login)
    if Config("app.itemCollectionTopLever.switch"):
        for i in range(4):
            taskQueue.push(FindAdventure, "hasItemsCollectionButton")
            taskQueue.push(beforeTopLeverItemCollection)
            taskQueue.push(inTopLeverItemCollection)
        taskQueue.push(backMain)
    if Config("app.refinery.switch"):
        taskQueue.push(BeforeRefinery)
        taskQueue.push(InRefinery)
        taskQueue.push(backMain)
    if Config("app.refinery.switch"):
        taskQueue.push(beforeInGuild)
        taskQueue.push(donate)
        taskQueue.push(getReward)
        taskQueue.push(backMain)
    # if Config("app.worldTree.switch"):
    # if Config("app.relic.switch"):

    threading.Thread(target=taskQueue.run, daemon=True).start()

    return {
        "code":0,
        "msg":"success"
    }

@api_bp.route('/api/stopRun', methods=['POST'])
def stopRun():
    """
    停止任务
    :return:
    """
    # 1 读取配置开始编排任务
    # - 高难度每日
    # - 矿厂每日
    # - 世界树
    def stop():
        raise Exception("human click stop")

    threading.Thread(target=stop, daemon=True).start()

    return {
        "code":0,
        "msg":"success"
    }