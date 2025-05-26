import time

from act.facades.Detect.Common.ErrorDetect import ErrorDetect
from act.facades.Detect.Common.FlashBattleDetect import FlashBattleDetect
from act.facades.Detect.Items.ItemsDetect import ItemsDetect
from act.facades.Emulator.Emulator import Click, UpdateSnapShot, Text, Pipe
from act.facades.Logx.Logx import logx


def beforeTopLeverItemCollection():
    """
    困难素材地图选择
    :return:
    """
    item = ItemsDetect()

    times  = 20
    while times > 0:
        UpdateSnapShot()
        # 剩余次数
        _, ok = item.zeroNum()
        if ok:
            break
        pot, ok = item.checkSkipFormat()
        if ok:
            Click(pot)
            logx.info("解除跳过编队")
            times  = 20
            continue
        resp,ok = item.hasTopLeverButton()
        if ok:
            Click(resp['pot'])

            logx.info("点击绝境III")
            Click((523, 278))

            # Click((715, 359))
            # logx.info("点击绝境IV")

            Click((1110, 542), sleep=1)
            logx.info("点击开始表演")
            break
        times-=1
    pass

def inTopLeverItemCollection():
    """
    困难素材战斗中
    :return:
    """
    item = ItemsDetect()
    flash = FlashBattleDetect()
    lag = ErrorDetect()

    times  = 20
    while times > 0:
        UpdateSnapShot()
        _,ok = lag.loading()
        if ok:
            time.sleep(0.5)
            times = 20
            continue
        resp,ok = item.hasTopLeverButton()
        if ok:
            break
        resp, ok = flash.isLoading()
        if ok:
            time.sleep(1)
            times = 20
            continue
        windowPot,ok = item.openRepeatBattleWindow()
        if ok :
            logx.debug("windowsPot")
            logx.debug(windowPot)
            Click(windowPot['pot'])
        # 设置次数
        matchResp,ok = item.checkRepeatBattle()
        if ok :
            # [279, 435, 4, 6]
            Click((279,435))# 开启次数
            logx.debug("开启次数")
            # [836, 441, 5, 0]
            Click((836,441))# 激活输入框
            logx.debug("激活输入框")
            Text("5")
            Click((1192, 603))
            # [1192, 603, 7, 6]
            Click(matchResp['pot'])
            logx.debug("开始重复战斗")
            continue

        # 处理快闪战斗
        resp, ok = flash.exeFlashBattle()
        if ok:
            Click(resp['pot'], sleep=1)
            times = 20
            continue
        # 处理普通战斗
        resp, ok = flash.inComBat()
        if ok:
            times = 20
            time.sleep(0.5)
            continue
        resp, ok = flash.combatSuccess()
        if ok:
            Click(resp['pot'], sleep=1)
            times = 20
            time.sleep(0.5)
            continue
        times-=1
        logx.debug(f"剩余次数 {times}")
    logx.info("高难副本结束")

def ItemCollectionRepSetting():
    """
    普通素材-重复战斗设置
    :return:
    """
    def setInputCallBack():
        Text("99")
        Click((0.5,0.5))

    pic = Pipe()
    itemsDetect = ItemsDetect()
    (pic.waitAndClickThrough(itemsDetect.selectMap())
     .waitAndClickThrough(itemsDetect.goFormation)
     .waitUntil(itemsDetect.nowLoading, itemsDetect.openRepeatBattleWindow)
     .waitAndClick(itemsDetect.setLimit)
     .waitAndClickCallback(itemsDetect.setLimitInput,setInputCallBack)
     .waitAndClickThrough(itemsDetect.checkRepeatBattle))
    pass

def ItemCollectionInBattleWaitResult():
    itemsDetect = ItemsDetect()
    """
    普通素材-战斗中等待结果
    :return:
    """
    while True:
        resp, ok1 = itemsDetect.inBattle()
        if ok1:
            time.sleep(1)
            continue
        resp, ok2 = itemsDetect.nowLoading()
        if ok2:
            time.sleep(1)
            continue
        resp, ok3 = itemsDetect.battleResult()
        if ok3:
            Click((0.5,0.5))
            break
        if not any([ok1, ok2, ok3]):
            raise Exception("未知页面")

    pass