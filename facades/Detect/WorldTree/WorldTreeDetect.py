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
    def isInWorldTreeDifficultySelectWindow(self):
        """
        选择难度
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("difficulty.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"世界树bata2.0","pot":pot},ok

    def getLever(self):
        """
        获取当前世界树等级
        :return:
        """
        # 截取指定位置
        dewXY = GetSnapShot().img
        dewXY = dewXY[0:dewXY.shape[0], 0:dewXY]
        res = MyCnocr.ocr(img=dewXY)
        for roc in res:
            self.dew,num = int(roc["text"])

        return res

    def updateDew(self):
        """
        更新露水数量
        :return:
        """
        dewXY = GetSnapShot().img
        # 截取指定位置
        dewXY = dewXY[0:dewXY.shape[0], 0:dewXY]

        num = 0

        res = MyCnocr.ocr(img=dewXY)
        for roc in res:
            if roc["text"] == "露水数量":
                self.dew,num = int(roc["text"])

        return num
    @matchResult
    def hasBizarreCard(self) :
        """
        是否存在奇遇卡片可选
        :return:
        """
        res = MyCnocr.ocr(img=GetSnapShot().img)
        return res, len(res)>0

    @matchResult
    def isInWorldTreeEndWindow(self) :
        """
        世界树探索结束窗口
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTreeEnd.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"探索结束","pot":pot},ok

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
        path = IMG_PATH.joinpath("Main").joinpath("blessingList.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"游戏主界面","pot":pot},ok

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
        path = IMG_PATH.joinpath("WorldTree").joinpath("blessing.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"游戏主界面","pot":pot},ok

    @matchResult
    def canSeeDew(self):
        """
        露水
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("dewNum.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"露水数量","pot":pot},ok