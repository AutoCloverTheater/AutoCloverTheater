from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QDesktopWidget

from src.facades.Constant.Constant import IMG_PATH, ROOT_PATH, APP_PATH
from src.facades.Logx.Logx import logx
from pathlib import Path

def mainWindow(port = 8233):


    file_path = Path(APP_PATH.joinpath("webui/index.html"))  # 替换为你的文件路径

    content = file_path.read_text(encoding="utf-8").replace("http://localhost:8233", f"http://localhost:{port}")  # 读取文本文件

    window = (1000,720)

    # 启动应用
    app = QApplication([])
    app.setApplicationName("四叶草🍀小助手")
    app.setWindowIcon(QIcon(f'{IMG_PATH.joinpath("uiWindowIcon.jpg")}'))

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
    browser.show()

    # 运行应用
    app.exec_()

if __name__ == '__main__':
    mainWindow()