from src.facades.Env.Env import Env


def get_config():
    return {
        "appName":Env("APPNAME", "com.moefantasy.clover"),
        "emulatorType": Env("EMULATORTYPE", 'mumu'),# 模拟器类型
        "emulatorPath":Env("EMULATORPATH"),# 模拟器路径
        "addr":Env("ADDR", '127.0.0.1'),
        "serial":Env("SERIAL"),# mumu 模拟器可以通过多开管理工具通过索引找到设备,其他的可以通过本机地址+端口找到设备
        "account":Env("ACCOUNT"),# 账号
        "password":Env("PASSWORD"),# 密码
        "displayWidth":1280,# 设备宽
        "displayHeight":720,# 设备高
        "dpi":240,# 设备dpi
    }


if __name__ == "__main__":
    print(get_config())