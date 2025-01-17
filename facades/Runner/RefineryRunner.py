from airtest.core.api import click, swipe

from facades.Detect.Refinery.RefineryDetect import RefineryDetect
from facades.Emulator.Emulator import ConnectEmulator, UpdateSnapShot
from facades.Logx.Logx import logx
from facades.Runner.layout.LoginRunner import Login

def BeforeRefinery():
    worldTree = RefineryDetect()

    matchResult = True
    times = 0
    while 1:
        if times >= 3:
            matchResult = False
            logx.warning("跳过矿厂准备阶段")
            break
        # 更新截图
        UpdateSnapShot()
        # 查找冒险按钮
        adv,ok = worldTree.hasAdventureButton()
        if ok:
            click(adv['pot'])
            times = 0
            continue
        #     是否滑到底了
        isSwipToEnd,ok = worldTree.isSwipToEnd()
        if ok:
            # 从左向右滑动
            logx.info("从右向左滑动")
            swipe((200, 20), (400, 20), duration=0.5,times=5)
            times = 0
            continue
        # 查找冒险中的神秘矿厂
        refinery,ok = worldTree.hasRefineryEntrance()
        if ok:
            click(refinery['pot'])
        else:
            # 从右向左滑动
            logx.info("从右向左滑动")
            swipe((400, 20), (200, 20), duration=0.5,steps=2)
            times = 0
            continue
        # 在神秘矿厂内
        isInRefinery,ok = worldTree.isInRefinery()
        if ok:
            break
        return matchResult
def InRefinery():
    refinery = RefineryDetect()

    # 尝试识别今天是周几
    refinery.mathDate()

    refineryRoi = refinery.returnRefineryRoi()
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
        if ok:
            logx.warning("今日矿厂次数用光，跳过")
            break
        # 开始识别可以快闪的矿
        fast,ok = refinery.fastBattle()
        if ok:
            click(fast['pot'],duration=1)
            times = 0
            continue
    times +=1

    return matchResult



if __name__ == '__main__':
    ConnectEmulator()
    Login()
    BeforeRefinery()
    InRefinery()