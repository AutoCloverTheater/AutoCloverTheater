import yaml

from src.facades.Constant.Constant import ROOT_PATH
from src.facades.Logx.Logx import logx


class EnvDriver:
    data = {}

    def iniFromFile(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.data = yaml.safe_load(file)
        except FileNotFoundError:
            logx.error(f"文件 {file_path} 未找到")
        except yaml.YAMLError as exc:
            logx.error(f"读取YAML文件时出错: {exc}")
        return self

    def saveToFile(self, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.safe_dump(self.data, file, allow_unicode=True)
        except IOError as exc:
            logx.error(f"写入文件 {file_path} 时出错: {exc}")
        return self

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def setValue(self,key: str, value):
        self.data[key] = value
        return True

    def exist(self, key:str):
        return key in self.data
def Env(key: str, default=None):
    temp = default
    keyList = key.split(".")
    obj = EnvDriver().iniFromFile(ROOT_PATH.joinpath("env.yaml"))

    data = obj.data
    for i in keyList:
        if i in data :
            data = data.get(i)
            temp = data
    return temp

if __name__== "__main__":
    print(Env("worldTree.lever"))