import cv2

from facades.Constant.Constant import RUNTIME_PATH, IMG_PATH
from facades.Detect.BaseDetect import BaseDetect
from facades.Detect.DetectLog import matchResult
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgSearch import imgSearch


class MainWindowDetect:
    # 有注册按钮并且没有匹配到输入账号密码
    @matchResult
    def isNotNeedLogin(self):
        path = IMG_PATH.joinpath("Main").joinpath("needAccountToLogin.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"不需要账号密码","pot":pot},ok

    @matchResult
    def isNeedLogin(self):
        path = IMG_PATH.joinpath("Main").joinpath("pleaseInputAccount.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"需要账号密码","pot":pot},ok
    @matchResult
    def isInDailySignRewardWindow(self):
        path = IMG_PATH.joinpath("Main").joinpath("dailyReward.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"每日签到奖励","pot":pot},ok

    @matchResult
    def isInDailySignWindow(self):
        path = IMG_PATH.joinpath("Main").joinpath("dailySign.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"每日签到奖励","pot":pot},ok

    @matchResult
    def isMainWindow(self):
        path = IMG_PATH.joinpath("Main").joinpath("main.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"主页面待登录","pot":pot},ok

    @matchResult
    def isInGameUiWindow(self):
        path = IMG_PATH.joinpath("Main").joinpath("gameUi.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"游戏主ui","pot":pot},ok

    @matchResult
    def hasLoginButton(self):
        path = IMG_PATH.joinpath("Main").joinpath("loginButton.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"登录按钮","pot":pot},ok