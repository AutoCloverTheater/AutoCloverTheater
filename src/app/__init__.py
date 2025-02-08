from flask import Flask
from flask_cors import CORS
from threading import Lock, Event
from .api import *

app = Flask(__name__)
CORS(app)  # 启用 CORS
# 用于存储 SSE 客户端的连接
clients = {}
clients_lock = Lock()

# 用于触发发送数据的事件
send_event = Event()
data_queue = []

# 注册蓝图
app.register_blueprint(api_bp)