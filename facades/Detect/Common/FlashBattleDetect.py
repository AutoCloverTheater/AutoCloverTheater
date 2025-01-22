from facades.Constant.Constant import IMG_PATH
from facades.Detect.DetectLog import matchResult
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgRead import MyImread
from facades.Img.ImgSearch import imgSearchArea
from facades.Logx.Logx import logx


class FlashBattleDetect:
    @matchResult
    def isOpenFlashBattleClosed(self):
        """
        快闪表演勾选状态
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath('fastBattle').joinpath("flashBattleClosed__1153_497_114_25__1103_447_177_125.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot(), mainWindow, [1153, 497, 114, 25])
        return {"name":"快闪表演-关闭","pot":pot},ok
    @matchResult
    def isOpenSkipFormationClosed(self):
        """
        跳过编队勾选状态
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath('fastBattle').joinpath("skipFormationClosed__1155_549_114_23__1105_499_175_123.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot(), mainWindow, [1155, 549, 114, 23])
        return {"name":"跳过编队-关闭","pot":pot},ok
    @matchResult
    def isInSuccessFlashBattleWindow(self) :
        """
        快闪战斗胜利
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath('fastBattle').joinpath("battleSuccess__509_416_265_71__459_366_365_171.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot(), mainWindow, [509, 410, 268, 79])
        if ok:
            pot = (0.5, 0)
        return {"name":"快闪战斗胜利","pot":pot},ok

    @matchResult
    def inFastBattleWindow(self) :
        """
        快闪战斗中
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath('fastBattle').joinpath("inFastBattle__1099_172_20_92__1049_122_120_192.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot(), mainWindow, [1099, 172, 20, 92])
        if ok:
            pot = (0.5, 0)
        return {"name":"快闪战斗中。。。。","pot":pot},ok

    @matchResult
    def isInFailedFlashBattleWindow(self) :
        """
        快闪战斗失败
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath('fastBattle').joinpath("battleFailed_509_410_268_79_459_360_368_179.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot(), mainWindow, [509, 410, 268, 79])
        if ok:
            pot = (0.5, 0)
        return {"name":"快闪战斗失败","pot":pot},ok
    @matchResult
    def isInBattleResultWindow(self) :
        """
        是否打开了演出结算窗口
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath('fastBattle').joinpath("settlementBattle__502_40_280_63__452_0_380_153.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot(), mainWindow, [452, 0, 380, 153])
        if ok:
            pot = (0.5, 0)
        return {"name":"演出结算","pot":pot},ok

    @matchResult
    def isLoading(self) :
        """
        是否在加载中
        :return:
        """

        imgs = [
            'lag/lag__622_345_35_31__572_295_135_131.png',
            'lag/lag__576_400_136_35__526_350_236_135.png',
            'lag/loading__867_579_343_97__817_529_443_191.png',
        ]
        roi = [
            (622, 345, 35, 31),
            (576, 400, 136, 35),
            (867, 579, 343, 97),
        ]
        ok = False
        pot = (0, 0)

        for k, i in enumerate(imgs):
            loading = MyImread(IMG_PATH.joinpath(i))
            resp, ok  = imgSearchArea(GetSnapShot(), loading, roi[k])
            if ok:
                pot = resp[0]
                break

        return {"name":"正在加载...","pot":pot},ok

    @matchResult
    def startPerform(self):
        """
        开始表演
        :return:
        """
        path = IMG_PATH.joinpath("Main/fastBattle/startPerform__1041_647_128_30__991_597_228_123.png")
        loading = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot(), loading, [1041, 647, 128, 30], 0.99)
        if ok:
            pot = pot.pop()
        return {"name":"开始表演...","pot":pot},ok

    @matchResult
    def exeFlashBattle(self):
        """
        通用快闪战斗处理
        Returns:

        """
        imgs = [
            'flashBattleClosed__1153_497_114_25__1103_447_177_125.png',
            'skipFormationClosed__1155_549_114_23__1105_499_175_123.png',
            'battleSuccess__509_416_265_71__459_366_365_171.png',
            'inFastBattle__1099_172_20_92__1049_122_120_192.png',
            'battleFailed_509_410_268_79_459_360_368_179.png',
            'settlementBattle__502_40_280_63__452_0_380_153.png',
        ]
        roi = [
            [1153, 497, 114, 25],
            [1155, 549, 114, 23],
            [509, 410, 268, 79],
            [1099, 172, 20, 92],
            [509, 410, 268, 79],
            [502, 40, 280, 63],
        ]
        names = [
            "快闪表演-关闭",
            "跳过编队-关闭",
            "快闪战斗胜利",
            "快闪战斗中。。。。",
            "快闪战斗失败",
            "演出结算",
        ]
        pots = [
            (1128, 532),# flashBattleClosed
            (1129, 588),# skipFormationClosed
            (0.5, 0.0),# battleSuccess
            (0.5, 0.0),# inFastBattle
            (0.5, 0.0),# battleFailed
            (0.5, 0.0),# settlementBattle
        ]
        name = "未知"
        ok = False
        pot = []

        for k, i in enumerate(imgs):

            loading = MyImread(IMG_PATH.joinpath(f"Main/fastBattle/{i}"))
            resp, ok  = imgSearchArea(GetSnapShot(), loading, roi[k])
            if ok:
                if k >= 2:
                    pot = pots[k]
                else:
                    pot = resp[0]

                name = names[k]
                logx.info(f"{names[k]}")
                break

        return {"name":name,"pot":pot},ok