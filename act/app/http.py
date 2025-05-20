import sys
import traceback

from flask import request, jsonify

from act.app import app
from act.facades.Emulator.Emulator import UsefulEmulator

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
