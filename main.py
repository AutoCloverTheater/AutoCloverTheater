import ctypes
import logging
import sys
import threading

from src.app import app

from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QDesktopWidget

from src.facades.Constant.Constant import IMG_PATH, APP_PATH
from src.facades.Logx.Logx import logx
from pathlib import Path

logging.getLogger("flask").setLevel(logging.ERROR)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

port = 8233

def mainWindow(port = 8233):
    if sys.platform == "win32":
        myappid = "github.clover.auto3"  # 替换为你的唯一标识符
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    file_path = Path(APP_PATH.joinpath("webui/index.html"))  # 替换为你的文件路径

    content = file_path.read_text(encoding="utf-8").replace("http://localhost:8233", f"http://localhost:{port}")  # 读取文本文件

    window = (1000,720)

    # 启动应用
    app = QApplication([])
    app.setApplicationName("四叶草🍀小助手")
    icon = QIcon(f'{IMG_PATH.joinpath("uiWindowIcon.jpg")}')
    app.setStyle("Fusion")

    app.setWindowIcon(icon)

    # # 获取屏幕对象
    screen = QDesktopWidget().screenGeometry()

    # # 获取屏幕宽高
    screen_width = screen.width()  # 屏幕宽度
    screen_height = screen.height()  # 屏幕高度
    left_point = (
        int(screen_width/2) - int(window[0]/2),
        int(screen_height/2)- int(window[1]/2),
    )

    # 创建浏览器窗口
    browser = QWebEngineView()
    browser.setFixedSize(window[0], window[1])
    browser.setHtml(content)  # 渲染 HTML 内容
    # 设置窗口位置和大小（x, y, width, height）
    browser.setGeometry(left_point[0], left_point[1], window[0], window[1])  # 窗口左上角
    browser.setWindowIcon(icon)
    browser.show()


    # 运行应用
    app.exec_()

threading.Thread(target=app.run, kwargs={'port': port, 'threaded': True}, daemon=True).start()
logx.info(f"listing port at {port}")
mainWindow(port)
