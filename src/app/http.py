import logging
import os
from pathlib import Path
import sys
import threading
import time
import traceback

from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from threading import Lock, Event

from src.app import send_event, clients_lock, clients, data_queue, app
from src.config.app import get_config
from src.facades.Constant.Constant import ROOT_PATH
from src.facades.Emulator.Emulator import UsefulEmulator
from src.facades.Env.Env import EnvDriver



def generate(client_id):
    while True:
        send_event.wait(0.3)  # 等待事件触发
        send_event.clear()  # 清除事件

        with clients_lock:
            if client_id not in clients:
                break
        if data_queue:
            data = data_queue.pop(0)
        else:
            data = f"1"
        yield data

@app.route('/stream')
def stream():
    client_id = id(Response())
    response = Response(generate(client_id), mimetype='text/event-stream')

    with clients_lock:
        clients[client_id] = response
    return response

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


print_event = threading.Event()
print_thread = None
@app.route('/api/start', methods=['POST'])
def start():
    def print_time():
        while not print_event.is_set():
            print(time.strftime('%Y-%m-%d %H:%M:%S'))
            time.sleep(1)

    global print_thread
    if print_thread is None or not print_thread.is_alive():
        print_event.clear()
    print_thread = threading.Thread(target=print_time)
    print_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
    print_thread.start()
    return {
        "code":0,
        "msg":"success"
    }, 200
@app.route('/api/stop', methods=['POST'])
def stop():
    print_event.set()
    return {
        "code":0,
        "msg":"success"
    }, 200

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
