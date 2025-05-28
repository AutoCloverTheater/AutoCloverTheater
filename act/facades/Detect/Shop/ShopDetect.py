from act.facades.Constant.Constant import IMG_PATH
from act.facades.Emulator.Emulator import GetSnapShot
from act.facades.Img.ImgRead import MyImread
from act.facades.Img.ImgSearch import imgSearchArea


class ShopDetect:
    def manWindowShop(self):
        """
        主页面商店按钮
        :return:
        """
        path = IMG_PATH.joinpath("shop/shop__1118_550_33_41__1068_500_133_141.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot(), img, [1118,550,33,41])
        pot = (0,0)
        if ok :
            pot = rois[0]

        return {"name":"主页面商店按钮", "pot":pot}
    def shopPackage(self):
        """
        礼包商城
        :return:
        """
        path = IMG_PATH.joinpath("shop/shopPackage__837_77_185_46__787_27_285_146.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot(), img, [837,77,185,46])
        pot = (0,0)
        if ok :
            pot = rois[0]

        return {"name":"主页面商店按钮", "pot":pot}


    def freePackage(self):
        """
        福利礼包
        :return:
        """
        path = IMG_PATH.joinpath("shop/freePackage__403_555_134_27__353_505_234_127.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot(), img, [403,555,134,27])
        pot = (0,0)
        if ok :
            pot = rois[0]

        return {"name":"主页面商店按钮", "pot":pot}