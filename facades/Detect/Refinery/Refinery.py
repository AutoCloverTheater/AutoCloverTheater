from facades.Constant.Constant import IMG_PATH
from facades.Detect.DetectLog import matchResult
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgRead import MyImread
from facades.Img.ImgSearch import imgSearch
from facades.Logx.Logx import logx
from facades.Ocr.MyCnocr import MyCnocr


class Refinery:
    @matchResult
    def isInRefinery(self):
        path = IMG_PATH.joinpath("Main").joinpath("refineryUi.png")
        img = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot().img, img)
        return {"name":"神秘矿厂","pot":pot},ok

    @matchResult
    def isCloseFastFormation(self):
        path = IMG_PATH.joinpath("Main").joinpath("closeFastFormation.png")
        img = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot().img, img)
        return {"name":"神秘矿厂-快速编队未开启","pot":pot},ok

    def ocrTodayLimit(self):
        xy = GetSnapShot().img
        x,y = xy.shape[:2]
        xy = xy[300:400,150:x-150]
        res = MyCnocr.ocr_for_single_line(xy)

        resText = [item['text'] for item in res if item['score'] > 0.4 and item['text'] != '']
        logx.info(f"识别到今日次数:{resText}")

        return resText.pop()

    def ocrRefineryLever(self):
        """
        todo 这里预期是识别已经通关的然后返回快闪表演的坐标
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("refineryLever.png")
        img = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot().img, img)
        return {"name":"神秘矿厂-xxxx","pot":pot},ok