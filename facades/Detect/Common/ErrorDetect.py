from facades.Constant.Constant import IMG_PATH
from facades.Detect.DetectLog import matchResult
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgRead import MyImread
from facades.Img.ImgSearch import imgSearchArea


class ErrorDetect:
    @matchResult
    def error(self):
        """
        游戏出现未知错误
        :return:
        """
        path = IMG_PATH.joinpath("error/error__579_293_112_28__529_243_212_128.png")
        loading = MyImread(path)
        pot, ok  = imgSearchArea(GetSnapShot(), loading, [529,243,212,128], 0.99)
        if ok:
            pot = pot.pop()
        return {"name":"游戏出现未知错误...","pot":pot},ok

    @matchResult
    def gameUpdating(self):
        """
        服务器维护中
        """
        img = [
            {
                "url":"gameServiceUpdating__482_335_311_30__432_285_411_130.png",
                "roi":[482,335,311,30]
            },
            {
                "url": "gameServiceUpdating__552_321_168_27__502_271_268_127.png",
                "roi": [552,321,168,27]
            }
        ]
        pot = ()
        ok = False
        for item in img:
            path = IMG_PATH.joinpath(f"lag/{item['url']}")
            img = MyImread(path)
            pot, ok = imgSearchArea(GetSnapShot(), img, item["roi"])
            if ok:
                pot = pot[0]
                break

        return {"name":"服务器维护中","pot":pot},ok

    @matchResult
    def loading(self):
        """
        加载中
        :return:[]roi
        :return:bool
        """
        img = [
            {
                "url":"lag__622_345_35_31__572_295_135_131.png",
                "roi":[622, 345, 35, 31]
            },
            {
                "url": "lag__576_400_136_35__526_350_236_135.png",
                "roi": [576, 400, 136, 35]
            },            {
                "url": "loading__867_579_343_97__817_529_443_191.png",
                "roi": [867, 579, 343, 97]
            },
            {
                "url":"loading03__29_13_116_94__0_0_195_157.png",
                'roi': [29, 13, 116, 94]
            }
        ]
        pot = ()
        ok = False
        for item in img:
            path = IMG_PATH.joinpath(f"lag/{item['url']}")
            img = MyImread(path)
            pot, ok = imgSearchArea(GetSnapShot(), img, item["roi"])
            if ok:
                break

        return {"name": "加载中", "pot": pot}, ok