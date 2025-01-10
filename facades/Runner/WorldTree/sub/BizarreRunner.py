# 奇遇事件 - 原则上所有神器都不拿，商店也只是进去看看
from airtest.core.api import click

from facades.Detect.WorldTree.BizarreDetect import BizarreDetect
from facades.Logx import Logx


def bizarre():
    detect = BizarreDetect()

    matchResult = True
    # todo 有些事件结束后会返回上一个页面
    times = 0
    while 1:
        if times >= 3:
            matchResult = False
            break
        shopResp ,ok = detect.isInRabbitShopWindow()
        if ok:
            click((0,0))
        EncounteredEventResp,ok = detect.isInEncounteredEvent()
        if ok:
            click((0,0))
            continue
        isInSelectGift,ok= detect.isInSelectGift()
        if ok:
            click((0,0))
            continue
        isInEventNeedDew,ok = detect.isInEventNeedDew()
        if ok:
            click((0,0))
            continue
        isInSelectYourArtifact,ok = detect.isInSelectYourArtifact()
        if ok:
            click((0,0))
            continue

    return matchResult