from facades.Constant.Constant import IMG_PATH
from facades.Detect.DetectLog import matchResult
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgRead import MyImread
from facades.Img.ImgSearch import imgSearchArea


class AdventureDetect:
    @matchResult
    def isInMainUi(self):
        """
        游戏主页面
        :return:
        """
        path = IMG_PATH.joinpath("Main/adventure/adventure__773_622_65_86__723_572_165_148.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot(), mainWindow, [773,622,65,86])
        if ok:
            pot = pot.pop()
        return {"name":"游戏主界面ui","pot":pot},ok

    @matchResult
    def isInAdventureList(self):
        """
        冒险之旅
        :return:
        """
        path = IMG_PATH.joinpath("Main/adventure/adventureList__96_23_93_22__46_0_193_95.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot(), mainWindow, [96,23,93,22])
        if ok:
            pot = pot.pop()
        return {"name":"冒险之旅","pot":pot},ok

    @matchResult
    def hasWorldTreeButton(self):
        """
        世界树按钮
        :return:
        """
        path = IMG_PATH.joinpath("Main/adventure/worldTree.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot(), mainWindow, [0,336,1280,278])
        if ok:
            pot = pot.pop()
        return {"name":"世界树按钮","pot":pot},ok

    @matchResult
    def hasItemsCollectionButton(self):
        """
        素材收集
        :return:
        """
        path = IMG_PATH.joinpath("Main/adventure/itemsCollection.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot(), mainWindow, [0,336,1280,278])
        if ok:
            pot = pot.pop()
        return {"name":"素材收集","pot":pot},ok

    @matchResult
    def hasRelicButton(self):
        """
        遗迹
        :return:
        """
        path = IMG_PATH.joinpath("Main/adventure/relic.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot(), mainWindow, [0,336,1280,278])
        if ok:
            pot = pot.pop()
        return {"name":"遗迹","pot":pot},ok

    @matchResult
    def last(self):
        """
        甜蜜邀约-就是翻页到最后了
        :return:
        """
        path = IMG_PATH.joinpath("Main/adventure/sweetDate.png")
        mainWindow = MyImread(path)
        pots, ok  = imgSearchArea(GetSnapShot(), mainWindow, [0, 438, 1280, 278])
        if ok:
            pots = pots.pop()
        return {"name":"甜蜜邀约","pot":pots},ok