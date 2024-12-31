from facades.Env.Env import Env


def get_config():
    return {
        "emulatorType": Env("EmulatorType"),# 模拟器类型
        "emulatorPath":"/Applications/MuMuPlayer.app/Contents/MacOS",# 模拟器路径
        "serial":Env("Serial"),# mumu 模拟器可以通过多开管理工具通过索引找到设备,其他的可以通过本机地址+端口找到设备
        "account":Env("Account"),# 账号
        "password":Env("Password"),# 密码
    }