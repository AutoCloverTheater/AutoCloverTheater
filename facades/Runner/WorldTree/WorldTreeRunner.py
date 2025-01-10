import time
from airtest.core.api import click

from facades.Configs.Config import Config
from facades.Detect.FlashBattleDetect import FlashBattleDetect
from facades.Detect.WorldTree.BizarreDetect import AllowsCards
from facades.Detect.WorldTree.WorldTreeDetect import WorldTreeDetect
from facades.Emulator.Emulator import ConnectEmulator
from facades.Logx import Logx

def BeforeInWorldTree():
    worldTree = WorldTreeDetect()

    matchResult = True
    times = 0
    while 1:
        if times >= 3:
            matchResult = False
            break
        mainResp,ok = worldTree.isInMainWindow()
        if ok:
            Logx.info(f"准备点击冒险")
            adventureButton = (0, 0)
            click(adventureButton)
            Logx.info(f"点击冒险按钮，等待冒险列表")
            time.sleep(3)
            continue
        adventureListResp,ok = worldTree.isInAdventureListWindow()
        if ok:
            Logx.info(f"准备点击世界树")
            adventureListOfWorldTreeButton = (0, 0)
            click(adventureListOfWorldTreeButton)
            Logx.info(f"等待进入世界树")
            time.sleep(3)
            continue
        adventureMainResp, ok = worldTree.isInWorldTreeMainWindow()
        if ok:
            Logx.info(f"开始识别等级与分数")
            lever = worldTree.getLever()
            Logx.info(f"识别到等级:{lever}")
            if Config("app.worldTree.lever") > lever:
                Logx.info(f"等级符合，进入世界树")
                adventureMainResp.click((0, 0))
                time.sleep(3)
                continue
            else :
                Logx.info(f"等级不符合，退出世界树")
                break
    return matchResult
def AfterInWorldTree():
    # 记录等级
    pass

def InWorldTree():
    worldTree = WorldTreeDetect()
    FlashBattle = FlashBattleDetect()
    # 世界树进行中
    matchResult = True

    times = 0
    while 1:
        if times >= 3:
            matchResult = False
            break
        dewResp,ok = worldTree.canSeeDew()
        if ok:
            # 更新露水数量
            dew = worldTree.updateDew()
            Logx.info(f"当前露水：{dew}")

        # 开启快闪，跳过编队
        FlashBattleResp, ok = FlashBattle.isOpenFlashBattle()
        if not ok :
            click(FlashBattleResp['pot'])
            time.sleep(0.3)
            Logx.info(f"已跳过快闪")

        SkipFormationResp,ok = FlashBattle.isOpenSkipFormation()
        if not ok :
            click(SkipFormationResp['pot'])
            time.sleep(0.3)
            Logx.info(f"已跳过编队")

        isInFailedFlashBattleWindow,ok = FlashBattle.isInFailedFlashBattleWindow()
        if ok :
            click((0,0))
            time.sleep(1)
            Logx.info(f"战斗失败返回世界树主页")
            break
        isInSuccessFlashBattleWindow,ok = FlashBattle.isInSuccessFlashBattleWindow()
        if ok :
            Logx.info(f"战斗胜利")
            continue
        isInBattleResultWindow,ok = FlashBattle.isInBattleResultWindow()
        if ok :
            click((0,0))
            continue
        # 奇遇卡-这里最好使用ocr，然后再根据排序选择需要的卡
        BizarreCard,ok = worldTree.hasBizarreCard()
        if ok :
            # todo 这里写奇遇卡的处理逻辑
            cards = []
            for Card in BizarreCard:
                if Card['isSelected'] in AllowsCards:
                    cards.append(Card)
            # 排好优先级后选择第一个
            click(cards[0])
            Logx.info(f"选择奇遇卡：{cards[0]['name']}")
            # todo 可能会触发战斗

            # todo 没有触发战斗
            continue
        isInSelectYourBlessing, ok = worldTree.isInSelectYourBlessing()
        if ok:
            click((0,0))
            break

    return matchResult

if __name__ == '__main__':
    ConnectEmulator()