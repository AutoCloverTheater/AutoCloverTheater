import os
import sys
import subprocess
import time

# 定义常量
PYTHON_VERSION = "3.10"
VENV_DIR = os.path.join(os.getcwd(), "venv")  # 虚拟环境绝对路径

REQUIREMENTS_FILE = "requirements.txt"
FILES_TO_CHECK = ["requirements.txt", "main.py"]  # 需要检查的文件列表

if sys.platform == "win32":
    ExePath = os.path.join(VENV_DIR, "Scripts", "python")
else:
    ExePath = os.path.join(VENV_DIR, "bin", "python")


def check_python_version():
    """检查Python版本是否为3.10"""
    version = sys.version.split()[0]
    if version.startswith(PYTHON_VERSION):
        print(f"Python {PYTHON_VERSION} 已安装。")
        return True
    else:
        print(f"Python {PYTHON_VERSION} 未安装，当前版本为 {version}。")
        return False

def check_venv():
    """检查虚拟环境是否存在"""
    if os.path.isdir(VENV_DIR):
        print(f"虚拟环境 {VENV_DIR} 已存在。")
        return True
    else:
        print(f"虚拟环境 {VENV_DIR} 不存在。")
        return False

def create_venv():
    """创建虚拟环境"""
    try:
        print(f"创建虚拟环境 {VENV_DIR}...")
        subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True, capture_output=True,text=True)
        print(f"虚拟环境 {VENV_DIR} 创建完成。")
    except subprocess.CalledProcessError as e:
        print(f"创建虚拟环境失败：{e}")
    return False

def check_files():
    """检查文件完整性"""
    missing_files = [file for file in FILES_TO_CHECK if not os.path.exists(file)]
    if missing_files:
        print(f"以下文件缺失: {', '.join(missing_files)}")
        return False
    else:
        print("所有文件完整。")
        return True

def install_requirements():
    """安装依赖项"""
    print("安装依赖项...")
    subprocess.run([ExePath, "-m", "pip", "install", "-r", REQUIREMENTS_FILE], check=True, shell=True)
    print("依赖项安装完成。")

def check_requirements():
    """检查是否需要安装依赖项"""
    if os.path.exists(REQUIREMENTS_FILE):
        print("requirements.txt 存在，检查是否需要安装依赖项...")
        return True
    else:
        print("requirements.txt 不存在，跳过依赖项安装。")
        return False

def main():
    if not check_python_version():
        print("请安装 Python 3.10 后再运行此脚本。")
        return

    if not check_venv():
        create_venv()

    if not check_files():
        print("请确保所有文件完整后再运行此脚本。")
        return

    if check_requirements():
        install_requirements()

    print("安装引导程序执行完成。")
    # 启动一个新的 Python 进程来运行另一个脚本
    subprocess.Popen([ExePath, 'main.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 退出当前脚本
    sys.exit()

if __name__ == "__main__":
    main()