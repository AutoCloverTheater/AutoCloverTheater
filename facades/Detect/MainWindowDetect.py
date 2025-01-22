from facades.Constant.Constant import IMG_PATH
from facades.Detect.DetectLog import matchResult
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgRead import MyImread
from facades.Img.ImgSearch import imgSearch, imgSearchArea


class MainWindowDetect:
    # 输入账号密码
    @matchResult
    def pleaseInputAccount(self):
        path = IMG_PATH.joinpath("Main").joinpath("pleaseInputAccount.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot(), mainWindow)
        return {"name":"需要账号密码","pot":pot},ok
    @matchResult
    def isInDailySignRewardWindow(self):
        path = IMG_PATH.joinpath("Main").joinpath("dailyReward.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot(), mainWindow)
        return {"name":"每日签到奖励","pot":pot},ok

    @matchResult
    def isInDailySignWindow(self):
        path = IMG_PATH.joinpath("Main").joinpath("dailySign.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot(), mainWindow)
        return {"name":"每日签到奖励","pot":pot},ok

    @matchResult
    def isMainWindow(self):
        path = IMG_PATH.joinpath("Main").joinpath("main.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot(), mainWindow)
        return {"name":"主页面待登录","pot":pot},ok

    @matchResult
    def isInGameUiWindow(self):
        path = IMG_PATH.joinpath("Main").joinpath("gameUi.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot(), mainWindow)
        return {"name":"游戏主ui","pot":pot},ok

    @matchResult
    def hasLoginButton(self):
        path = IMG_PATH.joinpath("Main").joinpath("loginButton.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot(), mainWindow)
        return {"name":"登录按钮","pot":pot},ok
    @matchResult
    def userAgreementBotSelected(self):
        path = IMG_PATH.joinpath("Main/userAgreementBotSelected__408_394_35_39__358_344_135_139.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot(), mainWindow, [408,394,35,39])
        if ok:
            pot = pot[0]
        return {"name":"未勾选隐私协议","pot":pot},ok

    @matchResult
    def appStart(self):
        """
        游戏启动中
        """
        img = [
            {
                "url":"appStarted__558_300_401_80__508_250_501_180.png",
                "roi":[558,300,401,80]
            },
            {
                "url": "appStarted__45_659_178_27__0_609_273_111.png",
                "roi": [45,659,178,27]
            }
        ]
        pot = ()
        ok = False
        for item in img:
            path = IMG_PATH.joinpath(f"Main/{item['url']}")
            img = MyImread(path)
            pot, ok = imgSearchArea(GetSnapShot(), img, item["roi"])
            if ok:
                break

        return {"name":"游戏启动中","pot":pot},ok
