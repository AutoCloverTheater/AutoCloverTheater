import cv2

from facades.Constant.Constant import IMG_PATH
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgSearch import imgSearch


class BattleDetect:
    def beforeBattle(self):
        path = IMG_PATH.joinpath("Main").joinpath("beforeBattle.png")
        beforeBattle = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, beforeBattle)
        return pot, ok

    def battling(self):
        """
        战斗中
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("battling.png")
        battling = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, battling)
        return pot, ok

    def battleFailed(self):
        """
        战斗失败
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("battleFailed.png")
        battleFailed = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, battleFailed)
        return pot, ok

    def battleSuccess(self):
        """
        战斗成功
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("battleSuccess.png")
        battleSuccess = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, battleSuccess)
        return pot, ok