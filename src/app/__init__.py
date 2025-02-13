from flask import Flask
from flask_cors import CORS
from .api import *

app = Flask(__name__)
CORS(app)  # 启用 CORS

# 注册蓝图
app.register_blueprint(api_bp)
app.register_blueprint(sse_bp)