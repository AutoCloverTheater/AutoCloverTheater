from facades.Constant.Constant import IMG_PATH
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgRead import MyImread
from facades.Img.ImgSearch import imgSearchArea


class ErrorDetect:
    def error(self):
        """
        游戏出现未知错误
        :return:
        """
        path = IMG_PATH.joinpath("error/error__579_293_112_28__529_243_212_128.png")
        loading = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot().img, loading, [529,243,212,128], 0.99)
        if ok:
            pot = pot.pop()
        return {"name":"游戏出现未知错误...","pot":pot},ok