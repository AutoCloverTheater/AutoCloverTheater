import time

from airtest.core.api import click, swipe

from facades.Detect.Common.AdventureDetect import AdventureDetect
from facades.Emulator.Emulator import UpdateSnapShot, ConnectEmulator
from facades.Logx.Logx import logx

def findAdventure(callAdv:str):
    adv = AdventureDetect()

    # 检查是否有方法
    if hasattr(adv, callAdv):
        # 获取并调用方法
        method = getattr(adv, callAdv)
        logx.info(f"AdventureDetect 找到方法 {callAdv}")
    else:
        logx.error(f"AdventureDetect 没有找到方法 {callAdv}")
        return

    times = 0
    last = False
    while 1 :
        if times >= 5:
            logx.warning("跳过寻找入口")
            break
        UpdateSnapShot()
        # 是否翻到最后一页
        _, ok = adv.last()
        if ok:
            last = True
        # 游戏主界main
        resp,ok = adv.isInMainUi()
        if ok:
            click(resp['pot'])
            time.sleep(0.3)
            times = 0
            continue
        # 在冒险之旅，但是没有找到按钮
        AdventureListResp, inOk = adv.isInAdventureList()
        if not inOk:
            times +=1
            continue

        button,buttonOk = method()
        if inOk and buttonOk:
            click(button['pot'])
            time.sleep(0.3)
            times = 0
            break

        # 👈
        if last:
            logx.info("向前翻页")
            swipe((0.5, 0.5),(0.9, 0.5), duration=2)
            time.sleep(0.2)
            continue
        #  👉
        else:
            logx.info("向后翻页")
            swipe((0.9, 0.5),(0.5, 0.5), duration=2)
            time.sleep(0.2)
            continue

    times += 1

if __name__ == "__main__":
    ConnectEmulator()
    findAdventure("hasRelicButton")
    # findAdventure("hasItemsCollectionButton")
    # findAdventure("hasWorldTreeButton")