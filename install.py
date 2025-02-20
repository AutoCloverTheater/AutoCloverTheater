import os
import sys
import subprocess

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

def get_installed_packages():
    """获取当前环境已安装的包及版本"""
    if sys.platform == "win32":
        result = subprocess.run([ExePath, '-m', 'pip', 'list', '--format=freeze'], check=True, shell=True, capture_output=True, text=True)
    else:
        result = subprocess.run([ExePath, '-m', 'pip', 'list', '--format=freeze'], check=True, capture_output=True, text=True)
    packages = {}
    for line in result.stdout.splitlines():
        if '==' in line:
            pkg, version = line.split('==', 1)
            pkg = pkg.replace('-', '_')
            packages[pkg.lower()] = version.strip()
    return packages


def parse_requirements(file_path):
    """解析requirements.txt文件"""
    requirements = {}
    ignore = []
    error = []
    with open(file_path, 'r') as f:
        for row, line in enumerate(f):
            line = line.strip()
            if not line or line.startswith('#'):
                ignore.append(line)
                continue

            # 处理带版本号的包
            if '==' in line:
                pkg, spec = line.split('==', 1)
                pkg = pkg.replace('-', '_')
                requirements[pkg.lower()] = f'=={spec.strip()}'
            elif '@' not in line:  # 忽略非版本号格式
                error.append(line)
                print(f"解析失败: {line}")
    if len(ignore):
        for ignore_line in ignore:
            print(f"忽略行: {ignore_line}")

    if len(error):
        for err in error:
            print(f"解析失败: {err}")

    return requirements


def check_dependencies(file = 'requirements.txt'):
    """主检查函数"""
    installed = get_installed_packages()

    requirements = parse_requirements(file)

    missing_packages = []
    version_mismatch = []
    satisfied = []
    for pkg, spec in requirements.items():
        if  pkg not in installed:
            missing_packages.append(pkg)
            continue
        installed_ver = installed[pkg]
        try:
            # 构建版本规范 严格匹配指定版本
            spec_set = spec.split("=")
            if str(spec_set[-1]) != str(installed_ver):
                version_mismatch.append({
                    'package': pkg,
                    'required': spec,
                    'installed': installed_ver
                })
            else:
                satisfied.append(f"{pkg}=={installed_ver}")
        except Exception as e:
            print(f"版本检查错误: {pkg} - {e}")
    # 打印结果
    print("\n检查结果：")
    print(f"✅ 满足要求的包 ({len(satisfied)})：")
    print('\n'.join(satisfied))

    print(f"\n❌ 缺失的包 ({len(missing_packages)})：")
    print('\n'.join(missing_packages))

    print(f"\n⚠️ 版本不符的包 ({len(version_mismatch)})：")
    for item in version_mismatch:
        print(f"{item['package']} 需要 {item['required']} (已安装 {item['installed']})")

    return len(missing_packages) >0 or len(version_mismatch) > 0

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

    if check_dependencies(REQUIREMENTS_FILE):
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