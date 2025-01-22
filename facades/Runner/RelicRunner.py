import time

import imagehash
from PIL import Image
from airtest.core.api import click, swipe
from collections import Counter

from facades.Detect.Common.ErrorDetect import ErrorDetect
from facades.Detect.Common.FlashBattleDetect import FlashBattleDetect
from facades.Detect.Relic.RelicDetect import RelicDetect
from facades.Emulator.Emulator import UpdateSnapShot, ConnectEmulator, GetSnapShot
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

def _findNextNode():
    relic  = RelicDetect()
    UpdateSnapShot()
    # 在遗迹内
    _, inGame = relic.isInRelicGame()
    # 探索点
    resp, ok = relic.eventPoint()
    if ok and inGame:
        click(resp['pot'])
        time.sleep(5)
        return resp
    maps = [
        {
            "name":"右上角",
            "point":[(0.5,0.5),(0.1,0.9)],
        },{
            "name": "左上角",
            "point": [(0.5,0.5),(0.9,0.9)],
        },{
            "name": "右下角",
            "point": [(0.5,0.5),(0.1,0.1)],
        },{
            "name": "左下角",
            "point": [(0.5,0.5),(0.9,0.1)],
        }
    ]
    stop = False
    for item in maps:
        if stop:
            break
        name = item['name']
        point = item['point']
        # 在遗迹探索中
        _, ok = relic.isInRelicGame()
        if not ok:
            break

        # 视角复位
        UpdateSnapShot()
        resp, ok = relic.location()
        if ok:
            click(resp['pot'])
            time.sleep(0.2)
        else:
            logx.warning("没有找到复位按钮")
            return resp

        _, inBoss = relic.killedBoss()
        if inBoss:
            break

        for i in range(6):
            swipe(point[0], point[1])
            UpdateSnapShot()
            # 在遗迹内
            _, inGame = relic.isInRelicGame()
            if not inGame:
                break
            logx.info(f"{name}寻找第 {i + 1} 次")

            # 探索点
            resp, ok = relic.eventPoint()
            if ok:
                click(resp['pot'])
                UpdateSnapShot()
                # 在遗迹内
                _, inGame = relic.isInRelicGame()
                if not inGame:
                    break
                # 已经在boss点位
                _, inBoss = relic.killedBoss()
                if inBoss:
                    break
                _,ok = relic.reLocation()
                if ok :
                    stop = False
                    break
                else:
                    time.sleep(5)
                    stop = True
                    break

    # 视角复位
    UpdateSnapShot()
    resp, ok = relic.location()
    if ok:
        click(resp['pot'])
        time.sleep(0.5)
    else:
        logx.warning("没有找到复位按钮")
        return resp

    return resp

def ErikaMoving():
    """
    艾丽卡移动中
    连续三帧相同，则艾丽卡移动结束
    :return:
    """
    # [41,6,159,146]
    fpsLimit = 2

    fps = []
    while True:
        UpdateSnapShot()
        img = GetSnapShot().img
        Erika = img[6:6+146,41:41+159]

        hk = imagehash.average_hash(Image.fromarray(Erika))
        hk = f"{hk}"
        fps.append(hk)

        if len(fps) > fpsLimit:
            fps.pop(0)

        counts  = Counter(fps)
        if len(fps) == fpsLimit and len(counts) <= 1:
            logx.info("艾丽卡停止移动")
            break
        logx.info("艾丽卡移动中")


    return

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
        # 击杀boss了
        killedBoss, ok = relic.killedBoss()
        if ok:
            click(killedBoss['pot'])
            time.sleep(0.2)
            times = 0
            continue
        explorationEnds,ok = relic.explorationEnds()
        if ok:
            click(explorationEnds['pot'])
            time.sleep(1)
            break
        # 探索点
        resp, ok = relic.eventPoint()
        if ok and inGame:
            click(resp['pot'])
            ErikaMoving()
            times = 0
            continue
        # 没有找到探索点，开始寻找下一个探索点
        if not ok and inGame:
            _findNextNode()
            ErikaMoving()
            times = 0
            continue
        times+= 1

if __name__ == '__main__':
    def run():
        ConnectEmulator()
        Login()
        FindAdventure("hasRelicButton")
        beforeRelic()
        inRelic()

    for i in range(10):
        run()
        resp,ok = ErrorDetect().error()
        if ok :
            click(resp['pot'])
            run()