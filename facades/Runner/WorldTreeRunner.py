import time

from facades.Configs.Config import Config
from facades.Detect.Common.FlashBattleDetect import FlashBattleDetect
from facades.Detect.WorldTree.WorldTreeDetect import WorldTreeDetect
from facades.Emulator.Emulator import ConnectEmulator, UpdateSnapShot, Click
from facades.Logx.Logx import logx
from facades.Runner.core.Limit import error_function
from facades.Runner.layout.AdventureRunner import FindAdventure
from facades.Runner.layout.LoginRunner import Login

@error_function
def BeforeInWorldTree():
    """
    世界树冒险开始前
    :return:
    """

    worldTree = WorldTreeDetect()
    fastBattle = FlashBattleDetect()

    matchResult = True
    times = 0
    while 1:
        if times >= 3:
            matchResult = False
            logx.warning("跳过世界树准备阶段")
            break
        # 更新截图
        UpdateSnapShot()
        # 加载
        loading,ok = fastBattle.isLoading()
        if ok:
            time.sleep(1)
            continue
        # 识别等级
        _,ok = worldTree.isLeverMax()
        if ok:
            logx.info(f"已到达最大等级，退出世界树")
            break
        # 出发冒险按钮
        searchStartWorldTreeAdvButton, ok = worldTree.searchStartWorldTreeAdvButton()
        if ok and worldTree.lv < 50:
            Click(searchStartWorldTreeAdvButton['pot'])
            logx.info(f"点击出发冒险按钮，等待选择难度")
            times = 0
            continue
        # 选择难度
        leverSelect,ok = worldTree.hasTopLeverButton()
        if ok:
            Click(leverSelect['pot'])
            logx.info(f"选择难度")
            times = 0
            continue
        isLoading, ok = fastBattle.isLoading()
        if ok:
            time.sleep(1)
            times = 0
            continue
        startPerform, ok = worldTree.isInStartPerform()
        if ok:
            Click(startPerform['pot'])
            logx.info("开始表演")
            times = 0
            continue
        inGame, ok = worldTree.isInworldTreeCardWindow()
        if ok:
            time.sleep(0.1)
            break
        times +=1

    return matchResult
def AfterInWorldTree():
    # 记录等级
    pass
@error_function
def InWorldTree():
    """
    世界树入口选项
    :return:
    """
    worldTree = WorldTreeDetect()
    FlashBattle = FlashBattleDetect()

    matchResult = True

    times = 0
    while 1:
        if times >= 12:
            matchResult = False
            logx.warning("跳过世界树探索阶段")
            break
        # 更新截图
        UpdateSnapShot()
        # dewResp,ok = worldTree.canSeeDew()
        # if ok:
        #     # 更新露水数量
        #     dew = worldTree.updateDew()
        #     logx.info(f"当前露水：{dew}")

        # 开启快闪，跳过编队
        resp, ok = FlashBattle.isLoading()
        if ok:
            continue
        FlashBattleResp, ok = FlashBattle.exeFlashBattle()
        if ok :
            Click(FlashBattleResp['pot'], 0.4)
            continue
        # 选择
        Confirm, ok = worldTree.selectConfirm1()
        if ok:
            Click(Confirm['pot'], 0.3)
            times = 0
            continue
        # 赠礼
        wealthCard, ok = worldTree.wealthCard()
        if ok:
            Click(wealthCard['pot'])
        # 赠礼
        se,ok = worldTree.survivalCard()
        if ok:
            Click(se['pot'])
        # 赠礼
        lvPlus,ok = worldTree.lvPlusCard()
        if ok:
            Click(lvPlus['pot'])
        # 祝福
        isInSelectYourBlessing, ok = worldTree.isInSelectYourBlessing()
        if ok:
            Click(isInSelectYourBlessing['pot'])
        # 结束购买
        endBuy,ok = worldTree.hasEndBuyButton()
        if ok:
            Click(endBuy['pot'])
            times = 0
            continue
        # 放弃奖励
        givUpItem,ok = worldTree.giveUpItem()
        if ok:
            Click(givUpItem['pot'])

            times = 0
            continue
        # 处理遭遇事件
        event,ok = worldTree.hasEventConfirmButton()
        if ok:
            pot = event['pot'].pop(-1)
            Click(pot)

            times = 0
            continue
        # 获取奖励
        getItems,ok = worldTree.getItems()
        if ok:
            Click(getItems['pot'])

            times = 0
            continue
        # 探索结束
        isInWorldTreeEndWindow,ok = worldTree.isInWorldTreeEndWindow()
        if ok:
            Click((0,0))

            times = 0
            continue
        # 假设已经返回世界树冒险主页面
        isInWorldTree2,ok = worldTree.isInWorldTreeMainWindow()
        if ok:
            break
        exits, ok = worldTree.hasExit()
        if ok:
            Click(exits['pot'])
            times = 0
            continue
        # 探索中
        inGame, ok = worldTree.isInworldTreeCardWindow()
        if ok:
            times = 0
            time.sleep(0.5)
        # 奇遇卡
        BizarreCard, ok = worldTree.hasBizarreCard()
        if ok:
            pot = BizarreCard.pop(-1)
            Click(pot['pot'])
            times = 0
        reSelectResp, ok = worldTree.reSelect()
        if ok:
            pot = BizarreCard.pop()
            Click(pot['pot'])
            times = 0

        times += 1
        logx.warning(f"执行次数：{times}")

    return matchResult

if __name__ == '__main__':
    ConnectEmulator()
    Login()
    FindAdventure("hasWorldTreeButton")
    BeforeInWorldTree()
    InWorldTree()
