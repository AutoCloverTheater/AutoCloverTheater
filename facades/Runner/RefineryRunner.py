import time

from airtest.core.api import click, swipe

from facades.Detect.Common.BattleDetect import BattleDetect
from facades.Detect.Common.FlashBattleDetect import FlashBattleDetect
from facades.Detect.Refinery.RefineryDetect import RefineryDetect
from facades.Emulator.Emulator import ConnectEmulator, UpdateSnapShot
from facades.Logx.Logx import logx
from facades.Runner.layout.LoginRunner import Login


def find():
    UpdateSnapShot()
    Refinery = RefineryDetect()
    _, inAdvList = RefineryDetect().isInAdventureListWindow()

    Entrance, hasEntrance = Refinery.hasRefineryEntrance()
    if hasEntrance:
        click(Entrance['pot'])
        return

    while inAdvList and not hasEntrance:
        logx.info("正在寻找冒险按钮")
        swipe((1.0, 0.2), (0.5, 0.2), duration=2)
        time.sleep(2)
        UpdateSnapShot()
        Entrance, hasEntrance = Refinery.hasRefineryEntrance()
        if hasEntrance:
            click(Entrance['pot'])
            continue
        # 滑倒底了
        endOfLisRoi, ok = Refinery.isSwipToEnd()
        if ok:
            break

    while inAdvList and not hasEntrance:
        logx.info("正在寻找冒险按钮2")
        swipe((0.5, 0.2), (1.0, 0.2), duration=2)
        time.sleep(2)
        UpdateSnapShot()
        Entrance, hasEntrance = Refinery.hasRefineryEntrance()
        if hasEntrance:
            click(Entrance['pot'])
            continue
        _,inAdvList = Refinery.isInAdventureListWindow()




def BeforeRefinery():
    Refinery = RefineryDetect()

    matchResult = True
    times = 0

    while 1:
        if times >= 3:
            matchResult = False
            logx.warning("跳过矿厂准备阶段")
            break
        # 更新截图
        UpdateSnapShot()
        # 在神秘矿厂内
        isInRefinery,ok = Refinery.isInRefinery()
        if ok:
            logx.info("结束矿场准备阶段")
            break

        # 查找冒险按钮
        adv,ok = Refinery.hasAdventureButton()
        if ok:
            click(adv['pot'])
            times = 0
            continue

        # 查找冒险中的神秘矿厂
        # 没有找到开始向👉查找
        # 翻页到底了就开始向👈查找
        find()
        times+=1

    return matchResult
def InRefinery():
    refinery = RefineryDetect()
    fastBattle = FlashBattleDetect()

    # 尝试识别今天是周几
    weekday = refinery.mathDate()

    # 在神秘矿厂内
    _, ok = refinery.isInRefinery()
    refineryRoi = refinery.returnRefineryRoi()
    if ok and weekday == 6:
        logx.info("随机选择矿场")
        click(refineryRoi)

    matchResult = True
    times = 0
    while 1:
        if times >= 3:
            matchResult = False
            logx.warning("跳过矿厂冒险")
            break
        # 更新截图
        UpdateSnapShot()
        # 尝试识别今天的次数是否用光，用光了则跳过
        countToday,ok = refinery.isZeroCountForToday()
        if not ok:
            logx.warning("今日矿厂次数用光，跳过")
            break
        # 跳过编队
        FastFormation,ok = refinery.isCloseFastFormation()
        if ok:
            click(FastFormation['pot'])
            times = 0
            continue

        # 开始识别可以快闪的矿
        fast,ok = refinery.fastBattle()
        if ok:
            click((0,0))
            time.sleep(1)
            times = 0
            continue

        # 处理快闪
        resp,ok = fastBattle.isInBattleResultWindow()
        if ok:
            click(resp['pot'])
            times = 0
            continue
        resp,ok = fastBattle.isInFailedFlashBattleWindow()
        if ok:
            click(resp['pot'])
            times = 0
            continue
        resp,ok = fastBattle.isInSuccessFlashBattleWindow()
        if ok:
            click(resp['pot'])
            times = 0
            continue
        resp,ok = fastBattle.inFastBattleWindow()
        if ok:
            time.sleep(1)
            times = 0
            continue
        times += 1

    return matchResult



if __name__ == '__main__':
    ConnectEmulator()
    Login()
    BeforeRefinery()
    # InRefinery()