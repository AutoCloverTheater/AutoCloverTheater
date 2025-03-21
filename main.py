import ctypes
import logging
import os
import sys
import threading
import requests
import shutil
import zipfile

from src.app import app

from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QSizePolicy

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

    window = (1190,720)

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
    browser.setHtml(content)  # 渲染 HTML 内容
    # 设置窗口位置和大小（x, y, width, height）
    # 设置大小策略（关键）
    browser.setSizePolicy(
        QSizePolicy.Expanding,  # 水平策略
        QSizePolicy.Expanding  # 垂直策略
    )
    browser.setMinimumSize(window[0], window[1])
    browser.setGeometry(left_point[0], left_point[1], window[0], window[1])  # 窗口左上角
    browser.setWindowIcon(icon)
    browser.setAcceptDrops(False)
    browser.show()


    # 运行应用
    app.exec_()

threading.Thread(target=app.run, kwargs={'port': port, 'threaded': True}, daemon=True).start()
logx.info(f"listing port at {port}")
# while True:
#     logx.info(f"listing port at {port}")
#     logx.debug(f"listing port at {port}")
#     logx.warning(f"listing port at {port}")
#     logx.exception(f"listing port at {port}")
#     time.sleep(1)


def checkAdbutilsBinaries():
    FILE_PLATFORM = {
        "darwin": ["adb"],
        "linux": ["adb"],
        "win32": ["adb.exe", "AdbWinApi.dll", "AdbWinUsbApi.dll"],
    }

    import adbutils
    print(adbutils.__file__)  # 查看包路径，检查 binaries/ 目录

    path = Path(f"{adbutils.__file__}").parent.joinpath("binaries")

    for file in FILE_PLATFORM[sys.platform]:
        f = f"{path.joinpath(file)}"
        if os.path.exists(f) is True:
            return True
        else:
            copy_binaries(path, sys.platform)

    return True

BINARIES_URL = {
    "darwin": "https://dl.google.com/android/repository/platform-tools-latest-darwin.zip",
    "linux": "https://dl.google.com/android/repository/platform-tools-latest-linux.zip",
    "win32": "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
}
FNAMES_PER_PLATFORM = {
    "darwin": ["adb"],
    "linux": ["adb"],
    "win32": ["adb.exe", "AdbWinApi.dll", "AdbWinUsbApi.dll"],
}
def copy_binaries(target_dir, platform: str):
    assert os.path.isdir(target_dir)

    base_url = BINARIES_URL[platform]
    archive_name = os.path.join(target_dir, f'{platform}.zip')

    print("Downloading", base_url, "...", end=" ", flush=True)
    with open(archive_name, 'wb') as handle:
        response = requests.get(base_url, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    print("done")

    for fname in FNAMES_PER_PLATFORM[platform]:
        print("Extracting", fname, "...", end=" ")
        # extract the specified file from the archive
        member_name = f'platform-tools/{fname}'
        extract_archive_file(archive_file=archive_name, file=member_name, destination_folder=target_dir)
        shutil.move(src=os.path.join(target_dir, member_name), dst=os.path.join(target_dir, fname))

        # extracted files
        filename = os.path.join(target_dir, fname)
        if fname == "adb":
            os.chmod(filename, 0o755)
        print("done")

    os.rmdir(path=os.path.join(target_dir, 'platform-tools'))
    os.remove(path=archive_name)

def extract_archive_file(archive_file, file, destination_folder):
    extension = archive_file.rsplit('.', 1)[-1].lower()

    if extension == 'zip':
        with zipfile.ZipFile(archive_file, 'r') as archive:
            archive.extract(member=file, path=destination_folder)

mainWindow(port)