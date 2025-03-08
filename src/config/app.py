from src.facades.Env.Env import Env


def get_config():
    return {
        "appName":Env("APPNAME", "com.moefantasy.clover"),
        "emulatorType": Env("EMULATORTYPE", 'mumu'),# 模拟器类型
        "emulatorPath":Env("EMULATORPATH", ""),# 模拟器路径
        "addr":Env("ADDR", '127.0.0.1'), # 连接地址
        "serial":Env("SERIAL"),# mumu 模拟器可以通过多开管理工具通过索引找到设备,其他的可以通过本机地址+端口找到设备
        "account":Env("ACCOUNT"),# 账号
        "password":Env("PASSWORD"),# 密码
        "guildDonateLimit":Env("GUILD_DONATE_LIMIT", 3),# 工会捐献次数
        "itemCollection":{# 素材收集
            "switch": Env("ITEMCOLLECTION.SWITCH", False),
            "map": Env("ITEMCOLLECTION.MAP", "绝境IV"),
            "limit": Env("ITEMCOLLECTION.LIMIT", 3),
        },
        "itemCollectionTopLever":{# 高难度每日，打完为止
            "switch": Env("ITEMCOLLECTIONTOPLEVER.SWITCH", False),
            "lever": Env("ITEMCOLLECTIONTOPLEVER.LEVER", "绝境战IV"),
        },
        "relic":{
            "switch": Env("RELIC.SWITCH", False),
            "lever": Env("RELIC.LEVER", "普通难度"),
            "map": Env("RELIC.MAP", "沙漠星城"),
        },
        "refinery":{# 神秘矿厂每日，打完为止
            "switch": Env("REFINERY.SWITCH", False),
        },
        "worldTree":{# 世界树
            "switch": Env("WORLDTREE.SWITCH", False),
            "lever": Env("WORLDTREE.LEVER", "死境"),
        },
        "displayWidth":1280,# 设备宽
        "displayHeight":720,# 设备高
        "dpi":240,# 设备dpi
    }


if __name__ == "__main__":
    print(get_config())