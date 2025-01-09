import cv2

from facades.Constant.Constant import RUNTIME_PATH, IMG_PATH
from facades.Detect.BaseDetect import BaseDetect
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgSearch import imgSearch


class MainWindowDetect(BaseDetect):
    # 有注册按钮并且没有匹配到输入账号密码
    def isNotNeedLogin(self):
        path = IMG_PATH.joinpath("Main").joinpath("needAccountToLogin.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"不需要账号密码","pot":pot},ok
    def isNeedLogin(self):
        path = IMG_PATH.joinpath("Main").joinpath("pleaseInputAccount.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"需要账号密码","pot":pot},ok

    def isInDailySignWindow(self):
        path = IMG_PATH.joinpath("Main").joinpath("needAccountToLogin.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"每日登录奖励","pot":pot},ok

    def isMainWindow(self):
        path = IMG_PATH.joinpath("Main").joinpath("main.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"主页面待登录","pot":pot},ok