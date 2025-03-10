import cv2

from src.facades.Constant.Constant import IMG_PATH
from src.facades.Detect.DetectLog import matchResult
from src.facades.Emulator.Emulator import GetSnapShot
from src.facades.Img.ImgRead import MyImread
from src.facades.Img.ImgSearch import imgSearchArea
from src.facades.Ocr.MyCnocr import MyCnocr


class ItemsDetect:
    @matchResult
    def checkSkipFormat(self):
        """
        检查是否跳过编队
        :return:
        """
        img = {
            "url":"Main/normalBattle/skip__899_533_34_29__849_483_134_129.png",
            "roi": [899, 533, 34, 29]
        }

        template = MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"勾选了跳过编队", "pot":pot},ok
    @matchResult
    def openRepeatBattleWindow(self):
        """
        进入重复战斗设置窗口
        :return:
        """
        img = {
            "url":"Main/normalBattle/repeatBattle__1135_25_41_32__1085_0_141_107.png",
            "roi": [1135, 25, 41, 32]
        }
        template =MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"开始重复战斗", "pot":pot},ok

    @matchResult
    def checkRepeatBattle(self):
        """
        开始重复战斗
        :return:
        """
        img = {
            "url":"Main/normalBattle/startRepeatBattle__562_531_156_28__512_481_256_128.png",
            "roi": [562, 531, 156, 28]
        }
        template =MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"开始重复战斗", "pot":pot},ok
    @matchResult
    def startBattle(self):
        """
        开始表演
        :return:
        """
        img = {
            "url":"",
            "roi": [1059, 655, 81, 45]
        }
        template, ok =MyImread(img['url'])
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"开始表演", "pot":pot},ok

    @matchResult
    def hasTopLeverButton(self):
        """
        高难副本
        :return:
        """
        img = [
            {
                "url":"topLever__1066_666_50_29__1016_616_150_104.png",
                "roi":[1059,655,81,45]
            },
            {
                "url": "topLever__1069_666_47_27__1019_616_147_104.png",
                "roi": [1059,655,81,45]
            }
        ]
        pot = ()
        ok = False
        for item in img:
            path = IMG_PATH.joinpath(f"Main/itemCollection/{item['url']}")
            img = MyImread(path)
            pot, ok = imgSearchArea(GetSnapShot(), img, item["roi"], 0.95)
            if ok:
                pot = pot[0]
                break
        return {"name":"发现高难副本","pot":pot},ok

    @matchResult
    def zeroNum(self):
        """
        次数用尽
        :return:
        """
        pot = ()

        roc = [1098,419,60,32]

        img = GetSnapShot()
        img = img[roc[1]:roc[1] + roc[3], roc[0]:roc[0] + roc[2]]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ocr = MyCnocr.ocrNum(img)

        num = 0
        if len(ocr):
            if ocr[0]['text'] != '':
                num = int(ocr[0]['text'].replace("/3", ""))
        str = f"挑战次数 {num}"
        return {"name":str,"pot":pot},num<=0