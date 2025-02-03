import cv2

from src.facades.Constant.Constant import IMG_PATH
from src.facades.Detect.DetectLog import matchResult
from src.facades.Emulator.Emulator import GetSnapShot
from src.facades.Img.ImgRead import MyImread
from src.facades.Img.ImgSearch import imgSearchArea
from src.facades.Ocr.MyCnocr import MyCnocr


class ItemsDetect:

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