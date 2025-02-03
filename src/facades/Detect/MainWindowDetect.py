from src.facades.Constant.Constant import IMG_PATH
from src.facades.Detect.DetectLog import matchResult
from src.facades.Emulator.Emulator import GetSnapShot
from src.facades.Img.ImgRead import MyImread
from src.facades.Img.ImgSearch import imgSearch, imgSearchArea


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
    def needLogin(self):
        path = IMG_PATH.joinpath("Main/needLogin__1202_150_46_65__1152_100_128_165.png")
        img = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot(), img, [1202,150,46,65], 0.95)
        if ok:
            pot = pot[0]
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
        path1 = IMG_PATH.joinpath("Main/userAgreementBotSelected__408_394_35_39__358_344_135_139.png")
        path2 = IMG_PATH.joinpath("Main/userAgreementBotSelected__421_327_127_20__371_277_227_120.png")
        img1 = MyImread(path1)
        img2 = MyImread(path2)
        pot1, ok1  = imgSearchArea(GetSnapShot(), img1, [408,394,35,39])
        pot2, ok2  = imgSearchArea(GetSnapShot(), img2, [421,327,127,20])

        pot = ()
        ok = False
        if ok1 and ok2:
            ok = True
            pot = pot1[0]

        return {"name":"未勾选隐私协议","pot":pot},ok1 and ok

    @matchResult
    def dlc(self):
        """
        有新内容需要更新
        """
        path = IMG_PATH.joinpath("Main/Dlc__411_319_252_30__361_269_352_130.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot(), mainWindow, [411,319,252,30])
        if ok:
            # [716,482,54,28] //确认按钮的roi
            pot = (716,482)
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
            pot, ok = imgSearchArea(GetSnapShot(), img, item["roi"], 0.95)
            if ok:
                break

        return {"name":"游戏启动中","pot":pot},ok
