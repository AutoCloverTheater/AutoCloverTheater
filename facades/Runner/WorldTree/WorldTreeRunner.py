import time
from airtest.core.api import click

from facades.Configs.Config import Config
from facades.Detect.FlashBattleDetect import FlashBattleDetect
from facades.Detect.WorldTree.BizarreDetect import AllowsCards
from facades.Detect.WorldTree.WorldTreeDetect import WorldTreeDetect
from facades.Emulator.Emulator import ConnectEmulator, UpdateSnapShot
from facades.Logx import Logx
from facades.Runner.layout.LoginRunner import Login


def BeforeInWorldTree():
    worldTree = WorldTreeDetect()

    matchResult = True
    times = 0
    while 1:
        if times >= 3:
            matchResult = False
            break
        # 更新截图
        UpdateSnapShot()
        mainResp,ok = worldTree.isInMainWindow()
        if ok:
            Logx.info(f"准备点击冒险")
            adventureButton = (0, 0)
            click(adventureButton)
            Logx.info(f"点击冒险按钮，等待冒险列表")
            continue
        adventureListResp,ok = worldTree.isInAdventureListWindow()
        if ok:
            Logx.info(f"准备点击世界树")
            adventureListOfWorldTreeButton = (0, 0)
            click(adventureListOfWorldTreeButton)
            Logx.info(f"等待进入世界树")
            continue
        adventureMainResp, ok = worldTree.isInWorldTreeMainWindow()
        if ok:
            Logx.info(f"开始识别等级与分数")
            lever = worldTree.getLever()
            Logx.info(f"识别到等级:{lever}")
            if Config("app.worldTree.lever") > lever:
                Logx.info(f"等级符合，进入世界树")
                adventureMainResp.click((0, 0))
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
            time.sleep(0.1)
            Logx.info(f"已跳过快闪")

        SkipFormationResp,ok = FlashBattle.isOpenSkipFormation()
        if not ok :
            click(SkipFormationResp['pot'])
            time.sleep(0.1)
            Logx.info(f"已跳过编队")

        isInFailedFlashBattleWindow,ok = FlashBattle.isInFailedFlashBattleWindow()
        if ok :
            Logx.info(f"探索失败返回世界树主页")
            click(isInFailedFlashBattleWindow['pot'])
            break
        isInSuccessFlashBattleWindow,ok = FlashBattle.isInSuccessFlashBattleWindow()
        if ok :
            Logx.info(f"战斗胜利-点击下一步")
            click(isInSuccessFlashBattleWindow['pot'])
            continue
        isInBattleResultWindow,ok = FlashBattle.isInBattleResultWindow()
        if ok :
            Logx.info(f"战斗失败-点击下一步")
            click(isInBattleResultWindow['pot'])
            continue
        # 奇遇卡-这里最好使用ocr，然后再根据排序选择需要的卡
        BizarreCard,ok = worldTree.hasBizarreCard()
        if ok :
            # todo 这里写奇遇卡的处理逻辑
            cards = []
            for Card in BizarreCard:
                if Card['isSelected'] in AllowsCards:
                    cards.append(Card)
            if len(cards) == 0:
                Logx.error(f"没有可以选择的奇遇卡 ocr结果：{cards}")
                break
            # 排好优先级后选择第一个
            Logx.info(f"选择奇遇卡：{cards[0]['name']}")
            # 点击坐标是对角线的中点
            x = abs(cards[0]['position'][0][0] - cards[0]['position'][2][0] / 2)
            y = abs(cards[0]['position'][0][1] - cards[0]['position'][2][1] / 2)
            Logx.info(f"点击奇遇卡ocr对角线坐标：{x},{y}")
            click((x,y))
            time.sleep(1)
            continue
        isInSelectYourBlessing, ok = worldTree.isInSelectYourBlessing()
        if ok:
            click(isInSelectYourBlessing['pot'])
            break

    return matchResult

if __name__ == '__main__':
    ConnectEmulator()
    Login()
    BeforeInWorldTree()