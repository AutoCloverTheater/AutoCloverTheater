import time

from airtest.core.api import click

from facades.Detect.Common.AdventureDetect import AdventureDetect
from facades.Detect.Common.FlashBattleDetect import FlashBattleDetect
from facades.Detect.Relic.RelicDetect import RelicDetect
from facades.Emulator.Emulator import UpdateSnapShot, ConnectEmulator
from facades.Logx.Logx import logx
from facades.Runner.layout.AdventureRunner import FindAdventure
from facades.Runner.layout.LoginRunner import Login

def beforeRelic():
    relic = RelicDetect()
    fastBattle = FlashBattleDetect()
    times = 0
    while True:
        if times >= 5:
            logx.warning("跳过遗迹准备阶段")
            break
        UpdateSnapShot()
        go,ok = fastBattle.startPerform()
        if ok:
            click(go['pot'])
            times = 0
            time.sleep(0.1)
            continue
        _, ok = relic.isInRelicGame()
        if ok:
            time.sleep(0.3)
            break
        settingMap, ok = relic.hasSettingMap()
        if ok:
            click(settingMap['pot'])
            times = 0
            time.sleep(0.1)
        settingRank, ok = relic.hasSettingRank()
        if ok:
            click(settingRank['pot'])
            times = 0
            time.sleep(0.1)
        start,ok = relic.hasGoExplore()
        if ok:
            click(start['pot'])
            time.sleep(0.3)
            continue
        # 加载
        _,ok = fastBattle.isLoading()
        if ok:
            time.sleep(0.1)
            times = 0
            continue
        times += 1


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
            logx.info(f"点位 {resp}")
            click(resp['pot'])
            times = 0
            time.sleep(0.2)
            continue
        getItems, ok = relic.getItems()
        if ok:
            click(getItems['pot'])
            times = 0
            continue
        # 在遗迹内
        _, inGame = relic.isInRelicGame()
        # 确认按钮
        confirmButton,ok = relic.hasConfirmButton()
        if ok and inGame:
            click(confirmButton['pot'])
            time.sleep(0.2)
            times = 0
            continue
        hasSelectButton,ok =  relic.hasSelectButton()
        if ok:
            click(hasSelectButton['pot'])
            time.sleep(0.2)
            times = 0
            continue
        # 探索点
        resp, ok = relic.eventPoint()
        if ok and inGame:
            click(resp['pot'])
            times = 0
            time.sleep(2)
            continue
        # 没有找到探索点，开始寻找下一个探索点
        if not ok and inGame:
            logx.info("没有找到探索点，开始寻找下一个探索点")
            time.sleep(1)
            continue
        times+= 1

if __name__ == '__main__':
    ConnectEmulator()
    # UpdateSnapShot()
    # fast = FlashBattleDetect()
    # res = fast.isOpenFlashBattleClosed()
    # logx.info(res)
    # Login()

    # FindAdventure("hasRelicButton")
    # beforeRelic()
    inRelic()