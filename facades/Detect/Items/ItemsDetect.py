from facades.Constant.Constant import IMG_PATH
from facades.Detect.DetectLog import matchResult
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgRead import MyImread
from facades.Img.ImgSearch import imgSearchArea


class ItemsDetect:

    @matchResult
    def isInAdventureListWindow(self):
        """
        冒险之旅窗口
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("adventure").joinpath("adventureList__96_23_93_22__46_0_193_95.png")
        mainWindow = MyImread(path)
        pots, ok  = imgSearchArea(GetSnapShot(), mainWindow, [96, 23, 93, 22])
        if ok:
            pot = pots[0]
        else:
            pot = (46,0)
        return {"name":"冒险之旅","pot":pot},ok