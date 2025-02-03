from src.facades.Constant.Constant import IMG_PATH
from src.facades.Emulator.Emulator import GetSnapShot
from src.facades.Img.ImgRead import MyImread
from src.facades.Img.ImgSearch import imgSearchArea


class BackDetect:
    def findLastPageButton(self):
        """
        寻找左上角的返回上一页按钮
        """
        path = IMG_PATH.joinpath("lastpage/lastpage__23_18_35_31__0_0_108_99.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot(), mainWindow, [23, 18, 35, 31])
        if ok:
          pot = pot[0]

        return {"name": "返回上一页", "pot": pot}, ok