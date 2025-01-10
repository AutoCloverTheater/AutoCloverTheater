import cv2
import numpy

from facades.Constant.Constant import IMG_PATH
from facades.Detect.DetectLog import matchResult

from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgSearch import imgSearch
from facades.Ocr.MyCnocr import MyCnocr

"""
世界树，死境难度。
避战流派只打奇遇而且只会选第一个选项
"""
class WorldTreeDetect:
    dew = 0 # 露水数量

    def __init__(self):
        pass

    @matchResult
    def isInWorldTreeMainWindow(self):
        """
        在世界树探索bata2.0页面
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTreeBata.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"世界树bata2.0","pot":pot},ok

    @matchResult
    def isInWorldTreeLeverSelectWindow(self):
        """
        选择难度
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTreeBata.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"世界树bata2.0","pot":pot},ok

    def getLever(self):
        """
        获取当前世界树等级
        :return:
        """
        res = MyCnocr.ocr(img=GetSnapShot().img)
        return 0

    def updateDew(self):
        """
        更新露水数量
        :return:
        """
        res = MyCnocr.ocr(img=GetSnapShot().img)
        return 0
    @matchResult
    def hasBizarreCard(self) :
        """
        是否存在奇遇卡片可选
        :return:
        """
        res = MyCnocr.ocr(img=GetSnapShot().img)
        return res, len(res)>0
    @matchResult
    def hasRabbitShopCard(self, img : numpy.array) -> bool:
        """
        是否存在兔子商店卡
        :return:
        """
        return False
    @matchResult
    def hasDivinationRoomCard(self, img : numpy.array) -> bool:
        """
        是否存在占卜
        :return:
        """
        return False
    @matchResult
    def hasTreasureBoxCard(self, img : numpy.array) -> bool:
        """
        是否存在宝箱
        :return:
        """
        return False
    @matchResult
    def hasRelaxCard(self) -> bool:
        """
        是否存在休息卡
        :return:
        """
        return False

    @matchResult
    def hasEliteBattleCard(self) -> bool:
        """
        是否存在精英战卡
        :return:
        """
        return False

    @matchResult
    def hasBattleCard(self) -> bool:
        """
        是否存在战斗卡
        :return:
        """
        return False

    @matchResult
    def isInWorldTreeEndWindow(self)->bool :
        """
        世界树探索结束窗口
        :return:
        """
        return False

    @matchResult
    def isInWorldTreeBattleReadyWindow(self):
        """
        世界树探索战斗准备窗口
        :return:
        """
        pass

    @matchResult
    def isInAdventureListWindow(self):
        """
        冒险列表窗口
        :return:
        """
        pass

    @matchResult
    def isInMainWindow(self):
        """
        游戏主页面
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("inGaminMainWindow.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"游戏主界面","pot":pot},ok

    @matchResult
    def isInSelectYourBlessing(self):
        """
        选择你的祝福
        1 提升4点速度降低5%防御
        2 获得50点露水
        3 回复6%生命2会合降低10%暴伤
        4 提升1.5%攻防生命
        :return:
        """
        return False

    @matchResult
    def canSeeDew(self):
        """
        露水
        :return:
        """
        pass