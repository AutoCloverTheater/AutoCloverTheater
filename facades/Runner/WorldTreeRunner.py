import time

from airtest.core.api import text, click, connect_device
from facades.Configs.Config import Config
from facades.Detect.FlashBattleDetect import FlashBattleDetect
from facades.Detect.MainWindowDetect import MainWindowDetect
from facades.Detect.WorldTree.WorldTreeDetect import WorldTreeDetect
from facades.Emulator.Emulator import UpdateSnapShot, ConnectEmulator
from facades.Logx import Logx
from facades.Runner.Runner import Runner


class WorldTreeRunner(Runner):
    def run(self):
        main = MainWindowDetect()
        worldTree = WorldTreeDetect()
        FlashBattle = FlashBattleDetect()
        while 1 and self.isStop == False:
            # 更新截图
            UpdateSnapShot()
            # 登录页面-需要登录
            loginNeedAccountAndPass, isNeedLoginOk = main.isNeedLogin()
            if isNeedLoginOk :
                Logx.info(f"识别到页面:{loginNeedAccountAndPass['name']}")
                Logx.info(f"输入账号")
                accountInput = (460,210)
                click(accountInput)
                time.sleep(1)
                text(Config("app").get("account"))
                Logx.info(f"输入账号完毕")
                passwordInput = (460, 280)
                Logx.info(f"输入密码")
                click(passwordInput)
                time.sleep(1)
                text(Config("app").get("password"))
                Logx.info(f"输入账号完毕")
                # 等待登录完成
                break
            # 登录页面-不需要登录
            isNotNeedLoginResp, ok = main.isNotNeedLogin()
            if ok and not isNeedLoginOk:
                Logx.info(f"识别到页面:{isNotNeedLoginResp['name']}")
                main.click(isNotNeedLoginResp['pot'])
                Logx.info(f"点击登录")
                continue
            # 每日签到
            sign, ok = main.isInDailySignWindow()
            if ok :
                Logx.info(f"识别到页面:{sign['name']}")
                click(sign['pot'])
                continue
            # 主页面
            isMainWindowResp, ok = main.isMainWindow()
            if ok :
                Logx.info(f"识别到页面:{isMainWindowResp['name']}")
                # y坐标增加60
                clickXy = (isMainWindowResp['pot'][0], isMainWindowResp['pot'][1] + 60)
                click(clickXy)
                Logx.info(f"预测下一个页面，点击登录")
                continue
        # 寻找冒险图片，然后点击

        # 在冒险列表寻找世界树图片，然后点击

        # 世界树准备战斗
        # while 1 and self.isStop == False:
        #     # 更新截图
        #     UpdateSnapShot()
        #     # 在世界树探索bata2.0页面
        #     worldTreeMain, ok = worldTree.isInWorldTreeMainWindow()
        #     if ok :
        #         Logx.info(f"识别到页面:{worldTreeMain['name']}")
        #         # 识别等级
        #         Logx.info(f"识别到等级:{worldTree.getLever()}")
        #         if worldTree.getLever() >= 50:
        #             Logx.info(f"等级大于等于50，退出世界树")
        #             break
        #     worldTreeLeverSelect, ok = worldTree.isInWorldTreeLeverSelectWindow()
        #     if ok :
        #         Logx.info(f"识别到页面:{worldTreeLeverSelect['name']}")
        #         worldTreeLeverSelect.click((0,0))
        #
        #     worldTreeBattleReady, ok = worldTree.isInWorldTreeBattleReadyWindow()
        #     if ok :
        #         # 编队页面
        #         Logx.info(f"识别到页面:{worldTreeBattleReady['name']}")
        #         worldTreeBattleReady.click((0,0))
        #
        # # 世界树进行中
        # while 1 and self.isStop == False:
        #     # 更新截图
        #     UpdateSnapShot()
        #     # 更新露水数量
        #     dew = worldTree.updateDew()
        #     Logx.info(f"当前露水：{dew}")
        #
        #     # 开启快闪，跳过编队
        #     worldTreeBattleReady, ok = FlashBattle.isFlashBattle()
        #     if not ok :
        #         Logx.info(f"识别到页面:{worldTreeBattleReady['name']}")
        #         worldTreeBattleReady.click((0,0))
        #         continue
        #     isSkipFormation,ok = FlashBattle.isSkipFormation()
        #     if ok :
        #         Logx.info(f"识别到页面:{isSkipFormation['name']}")
        #         isSkipFormation.click((0,0))
        #         continue
        #     isInFailedFlashBattleWindow,ok = FlashBattle.isInFailedFlashBattleWindow()
        #     if ok :
        #         Logx.info(f"识别到页面:{isInFailedFlashBattleWindow['name']}")
        #         Logx.info(f"战斗失败返回世界树主页")
        #         isInFailedFlashBattleWindow.click((0,0))
        #         break
        #     isInSuccessFlashBattleWindow,ok = FlashBattle.isInSuccessFlashBattleWindow()
        #     if ok :
        #         Logx.info(f"识别到页面:{isInSuccessFlashBattleWindow['name']}")
        #         isInSuccessFlashBattleWindow.click((0,0))
        #         continue
        #     isInBattleResultWindow,ok = FlashBattle.isInBattleResultWindow()
        #     if ok :
        #         Logx.info(f"识别到页面:{isInBattleResultWindow['name']}")
        #         isInBattleResultWindow.click((0,0))
        #         continue
        #
        #     # 奇遇卡-这里最好使用ocr，然后再根据排序选择需要的卡
        #     hasBizarreCard,ok = worldTree.hasBizarreCard()
        #     if ok :
        #         Logx.info(f"识别到奇遇卡:{hasBizarreCard}")
        #         hasBizarreCard.click((0,0))
        #         continue
        #
        #     # 奇遇事件 - 原则上所有神器都不拿，商店也只是进去看看
        #     isInRabbitShopWindow,ok = worldTree.subWindow.isInRabbitShopWindow()
        #     if ok :
        #         Logx.info(f"识别到页面:{isInRabbitShopWindow['name']}")
        #         isInRabbitShopWindow.click((0,0))
        #         continue
        #     isInSelectGift,ok = worldTree.subWindow.isInSelectGift()
        #     if ok :
        #         Logx.info(f"识别到页面:{isInSelectGift['name']}")
        #         isInSelectGift.click((0,0))
        #         continue
        #     isInEncounteredEvent,ok = worldTree.subWindow.isInEncounteredEvent()
        #     if ok :
        #         Logx.info(f"识别到页面:{isInEncounteredEvent['name']}")
        #         isInEncounteredEvent.click((0,0))
        #         continue
        #     isInSelectYourArtifact,ok = worldTree.subWindow.isInSelectYourArtifact()
        #     if ok :
        #         Logx.info(f"识别到页面:{isInSelectYourArtifact['name']}")
        #         isInSelectYourArtifact.click((0,0))
        #         continue
        #     isInEventNeedDew,ok = worldTree.subWindow.isInEventNeedDew()
        #     if ok :
        #         Logx.info(f"识别到页面:{isInEventNeedDew['name']}")
        #         isInEventNeedDew.click((0,0))
        #         continue

if __name__ == '__main__':
    ConnectEmulator()
    runner = WorldTreeRunner()
    runner.run()