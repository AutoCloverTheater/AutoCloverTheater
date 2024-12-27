import cv2

from facades.Detect.BaseDetect import BaseDetect
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgSearch import imgSearch


class MainWindowDetect(BaseDetect):
    def isNotNeedLogin(self):
        notNeedLogin = cv2.imread("")
        pot, ok  = imgSearch(GetSnapShot(), notNeedLogin)
        return self,ok
    def isNeedLogin(self):
        needLogin = cv2.imread("")
        pot, ok  = imgSearch(GetSnapShot(), needLogin)
        return self,ok

    def isInDailySignWindow(self):
        return True

    def isMainWindow(self):
        mainWindow = cv2.imread("")
        pot, ok  = imgSearch(GetSnapShot(), mainWindow)
        return self,ok