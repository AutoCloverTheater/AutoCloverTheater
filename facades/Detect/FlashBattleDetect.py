import cv2
import numpy

from facades.Constant.Constant import IMG_PATH
from facades.Detect.DetectLog import matchResult
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgSearch import imgSearch


class FlashBattleDetect:
    @matchResult
    def isOpenFlashBattleClosed(self):
        """
        判断是否快闪表演
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath('fastBattle').joinpath("flashBattleClosed_1128_532_105_21__1078_482_202_121.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"快闪表演-关闭","pot":pot},ok
    @matchResult
    def isOpenSkipFormationClosed(self):
        """
        判断是否跳过编队
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath('fastBattle').joinpath("skipFormationClosed_1129_588_103_22__1079_538_201_122.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"跳过编队-关闭","pot":pot},ok
    @matchResult
    def isInSuccessFlashBattleWindow(self) :
        """
        快闪战斗胜利
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath('fastBattle').joinpath("battleFailed_509_410_268_79_459_360_368_179.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"快闪战斗胜利","pot":pot},ok
    @matchResult
    def isInFailedFlashBattleWindow(self) :
        """
        快闪战斗失败
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath('fastBattle').joinpath("battleFailed_509_410_268_79_459_360_368_179.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"快闪战斗失败","pot":pot},ok
    @matchResult
    def isInBattleResultWindow(self) :
        """
        是否打开了演出结算窗口
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath('fastBattle').joinpath("endGame_556_53_171_43__506_3_271_143.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"快闪战斗失败","pot":pot},ok