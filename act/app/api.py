import multiprocessing
import os.path
import sys
import time
from typing_extensions import deprecated

from flask import request, Blueprint, Response, stream_with_context

from act.config.app import get_config
from act.facades.App.App import data_queue, send_event, clients_lock, clients, setExecuted
from act.facades.Constant.Constant import ROOT_PATH, APP_PATH
from act.facades.Emulator.Emulator import ActivityEmulator
from act.facades.Env.Env import EnvDriver
from act.facades.Logx.Logx import logx
from test import collection, refinery, worldTree


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
@sse_bp.route('/sse')
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

    file_path = APP_PATH.joinpath("webui/index.html")  # 替换为你的文件路径

    content = file_path.read_text(encoding="utf-8")  # 读取文本文件
    return content,200
@api_bp.route('/new_page.css', methods=['GET'])
def css():
    file_path = APP_PATH.joinpath("webui/new_page.css")  # 替换为你的文件路径

    content = file_path.read_text(encoding="utf-8")  # 读取文本文件

    return Response(content, mimetype='text/css'),200

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

process = {
}

@api_bp.route('/api/startRun', methods=['POST'])
def startRun():
    """
    开始任务
    :return:
    """
    request_data = request.get_json()
    global process

    p = {
        'collection': multiprocessing.Process(target=collection.run),
        'refinery': multiprocessing.Process(target=refinery.run),
        'worldTree': multiprocessing.Process(target=worldTree.run),
        'collectionTop': multiprocessing.Process(target=collection.run),
    }

    if request_data['script'] not in p:
        return {
            "code":400400,
            "msg":"script not found"
        },400

    process[request_data['script']] = p[request_data['script']]
    a_process = process.get(request_data['script'])
    a_process.start()

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
    global process
    request_data = request.get_json()
    if request_data["script"] not in process:
        return {
            "code":400400,
            "msg":"script not found"
        },400

    a_process = process.get(request_data["script"])
    if a_process is not None:
        a_process.terminate()  # 终止进程
        logx.info(f'Stopped {request_data["script"]}')
    else:
        logx.info(f'{request_data["script"]} is not running')

    return {
        "code":0,
        "msg":"success"
    }