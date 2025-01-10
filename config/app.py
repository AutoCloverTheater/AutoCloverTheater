from facades.Env.Env import Env


def get_config():
    return {
        "emulatorType": Env("EMULATORTYPE"),# 模拟器类型
        "emulatorPath":Env("EMULATORPATH"),# 模拟器路径
        "serial":Env("SERIAL"),# mumu 模拟器可以通过多开管理工具通过索引找到设备,其他的可以通过本机地址+端口找到设备
        "account":Env("ACCOUNT"),# 账号
        "password":Env("PASSWORD"),# 密码
        "worldTree":{
            "lever":Env("worldTree.lever")
        }
    }