import yaml

from facades.Constant.Constant import ROOT_PATH
from facades.Logx import Logx


class EnvDriver:
    data = {}

    def iniFromFile(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.data = yaml.safe_load(file)
        except FileNotFoundError:
            Logx.error(f"文件 {file_path} 未找到")
        except yaml.YAMLError as exc:
            Logx.error(f"读取YAML文件时出错: {exc}")
        return self

    def saveToFile(self, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.safe_dump(self.data, file, allow_unicode=True)
        except IOError as exc:
            Logx.error(f"写入文件 {file_path} 时出错: {exc}")
        return self

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def exist(self, key:str):
        return key in self.data
def Env(key: str, default=None):
    env = EnvDriver().iniFromFile(ROOT_PATH.joinpath("env.yaml"))
    return env.get(key, default)