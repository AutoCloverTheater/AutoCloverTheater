import time

from pywinauto.mouse import click

from facades.Detect.Common.FlashBattleDetect import FlashBattleDetect
from facades.Detect.Relic.RelicDetect import RelicDetect
from facades.Emulator.Emulator import UpdateSnapShot, ConnectEmulator
from facades.Logx.Logx import logx
from facades.Runner.layout.LoginRunner import Login


def beforeRelic():
    relic = RelicDetect()
    while True:
        times = 0
        while 1:
            if times >= 5:
                logx.warning("跳过寻找遗迹冒险入口")
                break
        UpdateSnapShot()
        _,ok = relic.isInRelicEntrance()
        if ok:
            break

def inRelic():
    relic = RelicDetect()
    fastBattle = FlashBattleDetect()

    times = 0
    while True:
        if times >= 5:
            logx.warning("跳过遗迹冒险")
            break
        UpdateSnapShot()
        # 加载
        _,ok = fastBattle.isLoading()
        if ok:
            time.sleep(0.1)
            times = 0
            continue
        # 战斗
        resp, ok = fastBattle.exeFlashBattle()
        if ok:
            click(resp['pot'])
            times = 0
            continue
        # 在遗迹内
        _, inGame = relic.isInRelicGame()
        # 探索点
        resp, ok = relic.eventPoint()
        if ok and inGame:
            click(resp['pot'])
            times = 0
            continue
        # 没有找到探索点，开始寻找下一个探索点
        if not ok and inGame:
            logx.info("没有找到探索点，开始寻找下一个探索点")
            continue
        times+= 1

if __name__ == '__main__':
    ConnectEmulator()
    Login()
    beforeRelic()
    inRelic()