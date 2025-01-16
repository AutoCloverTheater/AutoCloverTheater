import time

from airtest.core.api import click, swipe

from facades.Configs.Config import Config
from facades.Detect.FlashBattleDetect import FlashBattleDetect
from facades.Detect.WorldTree.BizarreDetect import AllowsCards
from facades.Detect.WorldTree.WorldTreeDetect import WorldTreeDetect
from facades.Emulator.Emulator import ConnectEmulator, UpdateSnapShot
from facades.Logx.Logx import logx
from facades.Runner.layout.LoginRunner import Login


def BeforeInWorldTree():
    """
    世界树冒险开始前
    :return:
    """
    worldTree = WorldTreeDetect()

    matchResult = True
    times = 0
    while 1:
        if times >= 3:
            matchResult = False
            break
        # 更新截图
        UpdateSnapShot()
        mainResp,MainWindowOk = worldTree.isInMainWindow()
        if MainWindowOk:
            click(mainResp['pot'])
            logx.info("等待进入冒险")
            continue
        worldTreeButton,ok = worldTree.hasWorldTreeButton()
        if ok:
            click(worldTreeButton['pot'])
            logx.info(f"点击世界树按钮，等待选择世界树主页面")
            continue
        adventureListResp,ok = worldTree.isInAdventureListWindow()
        if ok:
            logx.info(f"开始滑动搜索世界树入口按钮")
            # 从右向左滑动
            swipe((400, 100), (200, 100), duration=0.2,steps=2)
            time.sleep(1)
            continue
        adventureMainResp, ok = worldTree.isInWorldTreeMainWindow()
        if ok:
            logx.info(f"开始识别等级与分数")
            lever = worldTree.getLever()
            logx.info(f"识别到等级：lv {lever}")
            if Config("app.worldTree.lever") > lever:
                logx.info(f"等级符合，进入世界树")
            else :
                logx.info(f"等级不符合，退出世界树")
                break
        # 出发冒险按钮
        searchStartWorldTreeAdvButton, ok = worldTree.searchStartWorldTreeAdvButton()
        if ok and worldTree.lv < Config("app.worldTree.lever"):
            click(searchStartWorldTreeAdvButton['pot'])
            logx.info(f"点击出发冒险按钮，等待选择难度")
            continue
        leverSelect,ok = worldTree.hasTopLeverButton()
        if ok:
            click(leverSelect['pot'])
            logx.info(f"等待进入世界树战斗")
            continue
        startPerform, ok = worldTree.isInStartPerform()
        if ok:
            click(startPerform['pot'])
            continue
        inGame, ok = worldTree.isInworldTreeCardWindow()
        if ok:
            logx.info(f"世界树游戏中")
            break
        times +=1

    return matchResult
def AfterInWorldTree():
    # 记录等级
    pass
def InWorldTree():
    """
    世界树进行中
    :return:
    """
    worldTree = WorldTreeDetect()
    FlashBattle = FlashBattleDetect()

    matchResult = True

    times = 0
    while 1:
        if times >= 3:
            matchResult = False
            break
        # 更新截图
        UpdateSnapShot()
        dewResp,ok = worldTree.canSeeDew()
        if ok:
            # 更新露水数量
            dew = worldTree.updateDew()
            logx.info(f"当前露水：{dew}")

        # 开启快闪，跳过编队
        FlashBattleResp, ok = FlashBattle.isOpenFlashBattleClosed()
        if ok :
            click(FlashBattleResp['pot'])
            time.sleep(0.1)
            logx.info(f"已跳过快闪")

        SkipFormationResp,ok = FlashBattle.isOpenSkipFormationClosed()
        if ok :
            click(SkipFormationResp['pot'])
            time.sleep(0.1)
            logx.info(f"已跳过编队")
        # todo 这下面的还没有验
        isInFailedFlashBattleWindow,ok = FlashBattle.isInFailedFlashBattleWindow()
        if ok :
            logx.info(f"探索失败返回世界树主页")
            click(isInFailedFlashBattleWindow['pot'])
            break
        isInSuccessFlashBattleWindow,ok = FlashBattle.isInSuccessFlashBattleWindow()
        if ok :
            logx.info(f"战斗胜利-点击下一步")
            click(isInSuccessFlashBattleWindow['pot'])
            continue
        isInBattleResultWindow,ok = FlashBattle.isInBattleResultWindow()
        if ok :
            logx.info(f"战斗失败-点击下一步")
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
                logx.error(f"没有可以选择的奇遇卡 ocr结果：{cards}")
                continue
            # 排好优先级后选择第一个
            logx.info(f"选择奇遇卡：{cards[0]['name']}")
            # 点击坐标是对角线的中点
            x = abs(cards[0]['position'][0][0] - cards[0]['position'][2][0] / 2)
            y = abs(cards[0]['position'][0][1] - cards[0]['position'][2][1] / 2)
            logx.info(f"点击奇遇卡ocr对角线坐标：{x},{y}")
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
    # InWorldTree()