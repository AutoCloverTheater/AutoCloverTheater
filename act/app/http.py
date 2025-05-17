import sys
import traceback

from flask import request, jsonify

from act.app import app
from act.facades.Emulator.Emulator import UsefulEmulator


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
