import cv2
import numpy

from facades.Constant.Constant import IMG_PATH
from facades.Detect.DetectLog import matchResult
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgRead import MyImread
from facades.Img.ImgSearch import imgSearch


class FlashBattleDetect:
    @matchResult
    def isOpenFlashBattleClosed(self):
        """
        快闪表演勾选状态
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath('fastBattle').joinpath("flashBattleClosed_1128_532_105_21__1078_482_202_121.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"快闪表演-关闭","pot":pot},ok
    @matchResult
    def isOpenSkipFormationClosed(self):
        """
        跳过编队勾选状态
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath('fastBattle').joinpath("skipFormationClosed_1129_588_103_22__1079_538_201_122.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"跳过编队-关闭","pot":pot},ok
    @matchResult
    def isInSuccessFlashBattleWindow(self) :
        """
        快闪战斗胜利
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath('fastBattle').joinpath("battleSuccess__509_416_265_71__459_366_365_171.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"快闪战斗胜利","pot":pot},ok

    @matchResult
    def inFastBattleWindow(self) :
        """
        快闪战斗中
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath('fastBattle').joinpath("inFastBattle__1099_172_20_92__1049_122_120_192.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"快闪战斗中。。。。","pot":pot},ok

    @matchResult
    def isInFailedFlashBattleWindow(self) :
        """
        快闪战斗失败
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath('fastBattle').joinpath("battleFailed_509_410_268_79_459_360_368_179.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"快闪战斗失败","pot":pot},ok
    @matchResult
    def isInBattleResultWindow(self) :
        """
        是否打开了演出结算窗口
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath('fastBattle').joinpath("settlementBattle__502_40_280_63__452_0_380_153.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"演出结算","pot":pot},ok