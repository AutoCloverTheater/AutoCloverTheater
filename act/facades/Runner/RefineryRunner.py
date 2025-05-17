import time

from act.facades.Detect.Common.FlashBattleDetect import FlashBattleDetect
from act.facades.Detect.Refinery.RefineryDetect import RefineryDetect
from act.facades.Emulator.Emulator import UpdateSnapShot, Click, Swipe
from act.facades.Logx.Logx import logx


def find():
    UpdateSnapShot()
    Refinery = RefineryDetect()
    _, inAdvList = RefineryDetect().isInAdventureListWindow()

    Entrance, hasEntrance = Refinery.hasRefineryEntrance()
    if hasEntrance:
        Click(Entrance['pot'])
        return

    while inAdvList and not hasEntrance:
        # 已经在矿厂就跳出循环
        isIn,ok = Refinery.isInRefinery()
        if isIn:
            break

        logx.info("正在寻找冒险按钮")
        Swipe((1.0, 0.2), (0.5, 0.2))
        time.sleep(2)
        UpdateSnapShot()
        Entrance, hasEntrance = Refinery.hasRefineryEntrance()
        if hasEntrance:
            Click(Entrance['pot'])
            continue
        # 滑倒底了
        endOfLisRoi, ok = Refinery.isSwipToEnd()
        if ok:
            break

    while inAdvList and not hasEntrance:
        logx.info("正在寻找冒险按钮2")
        Swipe((0.5, 0.2), (1.0, 0.2))
        time.sleep(2)
        UpdateSnapShot()
        Entrance, hasEntrance = Refinery.hasRefineryEntrance()
        if hasEntrance:
            Click(Entrance['pot'])
            continue
        _,inAdvList = Refinery.isInAdventureListWindow()




def BeforeRefinery():
    Refinery = RefineryDetect()

    matchResult = True
    times = 0

    while 1:
        if times >= 12:
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
            Click(adv['pot'])
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

    matchResult = True
    times = 0
    while 1:
        if times >= 12:
            matchResult = False
            logx.warning("跳过矿厂冒险")
            break
        # 更新截图
        UpdateSnapShot()
        resp,ok = fastBattle.isLoading()
        if ok:
            time.sleep(1)
            continue
        # 处理快闪
        resp, ok = fastBattle.exeFlashBattle()
        if ok:
            Click(resp['pot'], sleep=1)
            times = 0
            continue
        # 尝试识别今天的次数是否用光，用光了则跳过
        countToday,ok = refinery.isZeroCountForToday()
        if ok:
            break
        # 跳过编队
        FastFormation,ok = refinery.isCloseFastFormation()
        if ok:
            Click(FastFormation['pot'])
            times = 0
            continue

        # 开始识别可以快闪的矿
        fast,ok = refinery.fastBattle()
        if ok:
            Click(fast['pot'])
            time.sleep(1)
            times = 0
            continue
        times += 1

    return matchResult
