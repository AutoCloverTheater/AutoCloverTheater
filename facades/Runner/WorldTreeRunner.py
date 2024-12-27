import logging

from facades.Configs.Config import Config
from facades.Detect.FlashBattleDetect import FlashBattleDetect
from facades.Detect.MainWindowDetect import MainWindowDetect
from facades.Detect.WorldTree.WorldTreeDetect import WorldTreeDetect
from facades.Emulator.Emulator import UpdateSnapShot
from facades.Runner.Runner import Runner


class WorldTreeRunner(Runner):
    def run(self):
        main = MainWindowDetect()
        worldTree = WorldTreeDetect()
        FlashBattle = FlashBattleDetect()
        while 1 and self.isStop == False:
            # 更新截图
            UpdateSnapShot()

            # 登录页面-不需要登录
            loginNotNeedAccountAndPass, ok = main.isNotNeedLogin()
            if ok :
                logging.info(f"识别到页面:{loginNotNeedAccountAndPass.name}")
                main.click((0,0))
                logging.info(f"点击登录")
                continue
            # 登录页面-需要登录
            loginNeedAccountAndPass, ok = main.isNeedLogin()
            if ok :
                logging.info(f"识别到页面:{loginNeedAccountAndPass.name}")
                loginNeedAccountAndPass.input(Config.get("app").get("account"))
                logging.info(f"输入账号")
                loginNeedAccountAndPass.input(Config.get("app").get("password"))
                logging.info(f"输入密码")
                loginNeedAccountAndPass.click((0,0))
                logging.info(f"点击登录")
                continue
            # 每日签到
            sign, ok = main.isInDailySignWindow()
            if ok :
                logging.info(f"识别到页面:{sign.name}")
                main.click((0,0))
                continue
            # 主页面
            main, ok = main.isMainWindow()
            if ok :
                logging.info(f"识别到页面:{sign.name}")
                break
        # 寻找冒险图片，然后点击

        # 在冒险列表寻找世界树图片，然后点击

        # 世界树准备战斗
        while 1 and self.isStop == False:
            # 更新截图
            UpdateSnapShot()
            # 在世界树探索bata2.0页面
            worldTreeMain, ok = worldTree.isInWorldTreeMainWindow()
            if ok :
                logging.info(f"识别到页面:{worldTreeMain.name}")
                # 识别等级
                logging.info(f"识别到等级:{worldTree.getLever()}")
                if worldTree.getLever() >= 50:
                    logging.info(f"等级大于等于50，退出世界树")
                    break
            worldTreeLeverSelect, ok = worldTree.isInWorldTreeLeverSelectWindow()
            if ok :
                logging.info(f"识别到页面:{worldTreeLeverSelect.name}")
                worldTreeLeverSelect.click((0,0))

            worldTreeBattleReady, ok = worldTree.isInWorldTreeBattleReadyWindow()
            if ok :
                # 编队页面
                logging.info(f"识别到页面:{worldTreeBattleReady.name}")
                worldTreeBattleReady.click((0,0))

        # 世界树进行中
        while 1 and self.isStop == False:
            # 更新截图
            UpdateSnapShot()
            # 更新露水数量
            dew = worldTree.updateDew()
            logging.info(f"当前露水：{dew}")

            # 开启快闪，跳过编队
            worldTreeBattleReady, ok = FlashBattle.isFlashBattle()
            if not ok :
                logging.info(f"识别到页面:{worldTreeBattleReady.name}")
                worldTreeBattleReady.click((0,0))
                continue
            isSkipFormation,ok = FlashBattle.isSkipFormation()
            if ok :
                logging.info(f"识别到页面:{isSkipFormation.name}")
                isSkipFormation.click((0,0))
                continue
            isInFailedFlashBattleWindow,ok = FlashBattle.isInFailedFlashBattleWindow()
            if ok :
                logging.info(f"识别到页面:{isInFailedFlashBattleWindow.name}")
                logging.info(f"战斗失败返回世界树主页")
                isInFailedFlashBattleWindow.click((0,0))
                break
            isInSuccessFlashBattleWindow,ok = FlashBattle.isInSuccessFlashBattleWindow()
            if ok :
                logging.info(f"识别到页面:{isInSuccessFlashBattleWindow.name}")
                isInSuccessFlashBattleWindow.click((0,0))
                continue
            isInBattleResultWindow,ok = FlashBattle.isInBattleResultWindow()
            if ok :
                logging.info(f"识别到页面:{isInBattleResultWindow.name}")
                isInBattleResultWindow.click((0,0))
                continue

            # 奇遇卡-这里最好使用ocr，然后再根据排序选择需要的卡
            hasBizarreCard,ok = worldTree.hasBizarreCard()
            if ok :
                logging.info(f"识别到奇遇卡:{hasBizarreCard}")
                hasBizarreCard.click((0,0))
                continue

            # 奇遇事件 - 原则上所有神器都不拿，商店也只是进去看看
            isInRabbitShopWindow,ok = worldTree.subWindow.isInRabbitShopWindow()
            if ok :
                logging.info(f"识别到页面:{isInRabbitShopWindow.name}")
                isInRabbitShopWindow.click((0,0))
                continue
            isInSelectGift,ok = worldTree.subWindow.isInSelectGift()
            if ok :
                logging.info(f"识别到页面:{isInSelectGift.name}")
                isInSelectGift.click((0,0))
                continue
            isInEncounteredEvent,ok = worldTree.subWindow.isInEncounteredEvent()
            if ok :
                logging.info(f"识别到页面:{isInEncounteredEvent.name}")
                isInEncounteredEvent.click((0,0))
                continue
            isInSelectYourArtifact,ok = worldTree.subWindow.isInSelectYourArtifact()
            if ok :
                logging.info(f"识别到页面:{isInSelectYourArtifact.name}")
                isInSelectYourArtifact.click((0,0))
                continue
            isInEventNeedDew,ok = worldTree.subWindow.isInEventNeedDew()
            if ok :
                logging.info(f"识别到页面:{isInEventNeedDew.name}")
                isInEventNeedDew.click((0,0))
                continue