import time

import cv2

from src.facades.Detect.Common.ErrorDetect import ErrorDetect
from src.facades.Detect.Common.FlashBattleDetect import FlashBattleDetect
from src.facades.Detect.Items.ItemsDetect import ItemsDetect
from src.facades.Detect.MainWindowDetect import MainWindowDetect
from src.facades.Emulator.Emulator import ConnectEmulator, Click, UpdateSnapShot, GetSnapShot
from src.facades.Logx.Logx import logx
from src.facades.Runner.layout.AdventureRunner import FindAdventure
from src.facades.Runner.layout.Back import backMain
from src.facades.Runner.layout.LoginRunner import Login


def beforeTopLeverItemCollection():
    item = ItemsDetect()


    for i in range(20):
        UpdateSnapShot()
        # 剩余次数
        _, ok = item.zeroNum()
        if ok:
            break
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
    pass

def inTopLeverItemCollection():
    item = ItemsDetect()
    flash = FlashBattleDetect()
    lag = ErrorDetect()

    times  = 12
    while times > 0:
        UpdateSnapShot()
        _,ok = lag.loading()
        if ok:
            time.sleep(0.5)
            times = 10
            continue
        resp,ok = item.hasTopLeverButton()
        if ok:
            break
        resp, ok = flash.isLoading()
        if ok:
            time.sleep(0.5)
            times = 10
            continue
        # 处理快闪战斗
        resp, ok = flash.exeFlashBattle()
        if ok:
            Click(resp['pot'], sleep=1)
            times = 10
            continue
        # 处理普通战斗
        resp, ok = flash.inComBat()
        if ok:
            times = 10
            time.sleep(0.5)
            continue
        resp, ok = flash.combatSuccess()
        if ok:
            Click(resp['pot'], sleep=1)
            times = 10
            time.sleep(0.5)
            continue
        times-=1
        logx.info(f"剩余次数 {times}")
    logx.info("高难副本结束")

# 每日高难副本
if __name__ == '__main__':
    ConnectEmulator()

    Login()
    FindAdventure("hasItemsCollectionButton")

    for i in range(4):
        beforeTopLeverItemCollection()
        inTopLeverItemCollection()

    backMain()