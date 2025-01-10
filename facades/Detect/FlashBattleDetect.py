import cv2
import numpy

from facades.Constant.Constant import IMG_PATH
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgSearch import imgSearch


class FlashBattleDetect:
    def isOpenFlashBattle(self):
        """
        判断是否快闪表演
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("flashBattleClosed.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"快闪表演-false","pot":pot},ok

    def isOpenSkipFormation(self):
        """
        判断是否跳过编队
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("skipFormationClosed.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"跳过编队-false","pot":pot},ok

    def isInSuccessFlashBattleWindow(self)->bool :
        """
        快闪战斗胜利
        :return:
        """
        return False

    def isInFailedFlashBattleWindow(self)->bool :
        """
        快闪战斗失败
        :return:
        """
        return False

    def isInBattleResultWindow(self)->bool :
        """
        是否打开了演出结算窗口
        :return:
        """
        return False