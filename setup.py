import os
import shutil
import sys
import zipfile
import requests

from setuptools import setup, find_packages

from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        install.run(self)  # 调用原始安装逻辑
        print("检查adb可执行文件")
        checkAdbutilsBinaries()

def checkAdbutilsBinaries():
    FILE_PLATFORM = {
        "darwin": ["adb"],
        "linux": ["adb"],
        "win32": ["adb.exe", "AdbWinApi.dll", "AdbWinUsbApi.dll"],
    }

    import adbutils
    print(adbutils.__file__)  # 查看包路径，检查 binaries/ 目录

    from pathlib import Path
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

setup(
    name="act",
    version="1.0.10",
    packages=find_packages(),
    cmdclass={
        "install": CustomInstallCommand,
    },
)