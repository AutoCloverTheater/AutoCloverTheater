import traceback

from flask import Flask
from flask_cors import CORS
from threading import Lock, Event

from config.app import get_config
from facades.Constant.Constant import ROOT_PATH
from facades.Env.Env import EnvDriver

app = Flask(__name__)
CORS(app)  # 启用 CORS
# 用于存储 SSE 客户端的连接
clients = {}
clients_lock = Lock()

# 用于触发发送数据的事件
send_event = Event()
data_queue = []

def generate(client_id):
    while True:
        send_event.wait(1)  # 等待事件触发
        send_event.clear()  # 清除事件

        with clients_lock:
            if client_id not in clients:
                break
        if data_queue:
            data = data_queue.pop(0)
        else:
            data = f"data: {time.strftime("%Y-%m-%d %H:%M:%S")}\n\n"
        yield data

@app.route('/api/getEmulatorType', methods=['GET'])
def getEmulatorType():
    allName = UsefulEmulator[sys.platform]
    allIn =[]
    for name, className in enumerate(allName):
        allIn.append(name)
    return {
        "code":0,
        "message":"SUCCESS",
        "list":allIn
    }

@app.route('/api/getEmulatorList', methods=['GET'])
def getEmulatorList():
    data = request.get_json()
    allName = UsefulEmulator[sys.platform]
    className = allName[data.get("type")]()
    AllSerial = className.getAllSerial()
    allIn  =[]
    for serial in AllSerial:
        allIn.append({"name":serial.name,"serial":serial.index})

    return {
        "code":0,
        "message":"SUCCESS",
        "data":allIn
    }


import sys
import time

from flask import Flask, Response, render_template, request, jsonify
from flask_cors import CORS
from threading import Lock, Event

from facades.Emulator.Emulator import UsefulEmulator

app = Flask(__name__)
CORS(app)  # 启用 CORS
# 用于存储 SSE 客户端的连接
clients = {}
clients_lock = Lock()

# 用于触发发送数据的事件
send_event = Event()
data_queue = []

def generate(client_id):
    while True:
        send_event.wait(1)  # 等待事件触发
        send_event.clear()  # 清除事件

        with clients_lock:
            if client_id not in clients:
                break
        if data_queue:
            data = data_queue.pop(0)
        else:
            data = f"data: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        yield data

@app.route('/stream')
def stream():
    client_id = id(Response())
    response = Response(generate(client_id), mimetype='text/event-stream')

    with clients_lock:
        clients[client_id] = response
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trigger', methods=['POST'])
def trigger():
    data = f"data: 1223\n\n"
    with clients_lock:
        data_queue.append(data)
    send_event.set()
    return "Data sent!"

@app.route('/api/getEmulatorType', methods=['GET'])
def getEmulatorType():
    allName = UsefulEmulator[sys.platform]
    allIn = []
    for name, className in enumerate(allName):
        allIn.append(className)
    return jsonify({
        "code": 0,
        "message": "SUCCESS",
        "list": allIn
    })

@app.route('/api/getEmulatorList', methods=['GET'])
def getEmulatorList():
    data = request.get_json()

    allName = UsefulEmulator[sys.platform]
    className = allName[data.get("type")]()
    AllSerial = className.getAllSerial()
    allIn = []
    for serial in AllSerial:
        allIn.append({"name": serial.get("name"), "serial": serial.get("index")})

    return jsonify({
        "code": 0,
        "message": "SUCCESS",
        "data": allIn
    })

@app.route('/api/baseSetting', methods=['GET'])
def getBaseSetting():
    """
    获取模拟器设置
    :return:
    """
    return get_config()
@app.route('/api/baseSetting', methods=['POST'])
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
        "msg":"success"
    }


@app.errorhandler(Exception)
def handle_exception(e):
    # 打印异常信息以便调试
    app.logger.error(f"An error occurred: {e}", exc_info=True)
    # 获取详细的堆栈跟踪
    tb = traceback.format_exc()
    return jsonify({
        "code": 1000,
        "message": "An unexpected error occurred",
        "trace": tb
    }), 500

if __name__ == '__main__':
    app.run(port=8233)
