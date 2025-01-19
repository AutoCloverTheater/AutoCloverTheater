import time

from pywinauto.mouse import click

from facades.Detect.Common.FlashBattleDetect import FlashBattleDetect
from facades.Detect.Relic.RelicDetect import RelicDetect
from facades.Emulator.Emulator import UpdateSnapShot
from facades.Logx.Logx import logx


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
    while True:
        times = 0
        while 1:
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
            resp, ok = fastBattle.exeFlasBattle()
            if ok:
                click(resp['pot'])
                continue