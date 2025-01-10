import cv2

from facades.Constant.Constant import IMG_PATH
from facades.Detect.DetectLog import matchResult
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgSearch import imgSearch

AllowsCards = [
    "奇遇","宝箱","商店","占卜",
    "战斗","精英战斗"
]

class BizarreDetect:
    def __init__(self):
        """
        世界树二级页面
        """
        #初始化所需要的模板文件
        pass

    @matchResult
    def isInSelectYourArtifact(self):
        """
        是否在选神器界面
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("selectYourArtifact.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"选择神器","pot":pot},ok

    @matchResult
    def isInEventNeedDew(self):
        """
        遭遇事件需要打水
        1.露水大于x
        2.不喝了
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("eventNeedDew.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"遭遇事件-打水","pot":pot},ok

    @matchResult
    def isInSelectGift(self):
        """
        选择赠礼
        1 远见
        2 友爱
        3 生存
        :param:
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("selectGift.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"选择赠礼","pot":pot},ok

    def isInRabbitShopWindow(self):
        """
        是否打开了兔子商店窗口
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("rabbitShop.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"兔子商店","pot":pot},ok

    def isInEncounteredEvent(self):
        """
        是否打开了遭遇事件窗口
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("encounteredEvent.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"遭遇事件","pot":pot},ok
