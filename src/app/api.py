import sys
from pathlib import Path

from flask import request, Blueprint

from src.config.app import get_config
from src.facades.Constant.Constant import ROOT_PATH
from src.facades.Env.Env import EnvDriver


# 创建一个蓝图对象
api_bp = Blueprint('api', __name__)

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
    resp = get_config()
    resp['platform'] = sys.platform
    return resp,200
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
        "msg":"success"
    }