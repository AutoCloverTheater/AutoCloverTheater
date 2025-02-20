import os
import sys
import subprocess

import pkg_resources

# 定义常量
PYTHON_VERSION = "3.1"
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
        print(f"Python >= {PYTHON_VERSION}0 未安装，当前版本为 {version}。")
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
        subprocess.run(['python', "-m", "venv", VENV_DIR], check=True, capture_output=True,text=True)
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

def _check_requirements(requirements_file='requirements.txt'):
    """检查当前环境是否满足依赖要求"""
    try:
        with open(requirements_file, 'r', encoding='utf-8') as f:
            requirements = [
                line.strip()
                for line in f
                if line.strip() and not line.startswith(('#', '-'))
            ]
    except FileNotFoundError:
        print(f"错误：{requirements_file} 文件不存在")
        return False
    missing = []
    wrong_version = []
    satisfied = []
    for req_line in requirements:
        try:
            req = pkg_resources.Requirement.parse(req_line)
        except (ValueError, pkg_resources.RequirementParseError):
            print(f"警告：无法解析依赖项 '{req_line}'")
            continue
        try:
            dist = pkg_resources.get_distribution(req.name)
            if not dist in req:
                wrong_version.append(f"{dist.key}=={dist.version} (需要 {req.specifier})")
            else:
                satisfied.append(f"{dist.key}=={dist.version}")
        except pkg_resources.DistributionNotFound:
            missing.append(req.name)
    # 打印检查结果
    print("\n检查结果：")
    print(f"[✓] 已满足 {len(satisfied)} 个依赖项")
    for item in satisfied:
        print(f"  - {item}")
    if wrong_version:
        print(f"\n[!] 版本不符 {len(wrong_version)} 个：")
        for item in wrong_version:
            print(f"  - {item}")
    if missing:
        print(f"\n[×] 缺失 {len(missing)} 个依赖项：")
        for item in missing:
            print(f"  - {item}")
    return not (missing or wrong_version)

def install_requirements():
    """安装依赖项"""
    print("安装依赖项...")
    if sys.platform == "win32":
        subprocess.run([ExePath, "-m", "pip", "install", "-r", REQUIREMENTS_FILE], check=True, shell=True)
    else:
        subprocess.run([ExePath, "-m", "pip", "install", "-r", REQUIREMENTS_FILE], check=True)

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

    if check_requirements() is False:
        raise ValueError("requirements.txt 不存在，无法安装依赖项。")
    if _check_requirements() is False:
        print("依赖项不满足要求，正在尝试安装")
        install_requirements()

    # 启动一个新的 Python 进程来运行另一个脚本
    if sys.platform == "win32":
        subprocess.Popen([ExePath, 'main.py'], shell=True)
    else:
        subprocess.Popen([ExePath, 'main.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("安装引导程序执行完成。")
    # 退出当前脚本
    sys.exit()


if __name__ == "__main__":
    main()