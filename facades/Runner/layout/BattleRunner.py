import time

from airtest.core.api import click

from facades.Detect.Common.BattleDetect import BattleDetect
from facades.Logx import Logx


def runFlashBattle():
    Battle = BattleDetect()

    matchResult = 0
    while 1:

        battlingResp, ok = Battle.battling()
        if not ok:
            Logx.info(f"识别到:{battlingResp['name']}")
            break

        battleFailedResp, ok = Battle.battleFailed()
        if not ok:
            Logx.info(f"识别到:{battleFailedResp['name']}")
            break
        battleSuccessResp, ok = Battle.battleSuccess()
        if not ok:
            Logx.info(f"识别到:{battleSuccessResp['name']}")
            break
        beforeBattleResp, ok = Battle.beforeBattle()
        if not ok:
            Logx.info(f"识别到:{beforeBattleResp['name']}")
            break

    return  matchResult