import time

from src.facades.Detect.Common.ErrorDetect import ErrorDetect
from src.facades.Detect.Common.FlashBattleDetect import FlashBattleDetect
from src.facades.Detect.Items.ItemsDetect import ItemsDetect
from src.facades.Emulator.Emulator import Click, UpdateSnapShot, Text
from src.facades.Logx.Logx import logx


def beforeTopLeverItemCollection():
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
        # 设置次数
        pot,ok = item.checkRepeatBattle()
        if ok :
            Click((0,0))# 开启次数
            logx.debug("开启次数")
            Click((0,0))# 激活输入框
            logx.debug("激活输入框")
            Text("5")
            Click(pot)
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