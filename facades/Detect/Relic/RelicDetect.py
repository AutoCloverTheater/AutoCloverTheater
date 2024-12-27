import numpy

from facades.Detect.Relic.RelicSubWindow import RelicSubWindow

class BaseDetect:
    subWindow = RelicSubWindow

    def __init__(self):
        self.subWindow = RelicSubWindow()
    """
    遗迹
    """
    def isInRelicWindow(self, img : numpy.array) -> bool:
        """
        是否处于遗迹准备窗口
        :param img:
        :return:
        """
        return False
    def hasBattlePoint(self, img : numpy.array) -> bool:
        """
        窗口内是否存在战斗点
        :param img:
        :return:
        """
        return False
    def hasEliteBattlePoint(self, img : numpy.array) -> bool:
        """
        窗口内是否存在精英战斗点
        :param img:
        :return:
        """
        return False
    def hasBizarrePoint(self, img : numpy.array) -> bool:
        """
        窗口内是否存在奇遇点
        :param img:
        :return:
        """
        return False
    def hasBossPoint(self, img : numpy.array) -> bool:
        """
        窗口内是否存在boss战斗点
        :param img:
        :return:
        """
        return False

    def searchBossPoint(self, img : numpy.array) -> bool:
        """
        没有战斗点，没有奇遇点，打开小地图，寻找boss位置
        :param img:
        :return:
        """
        return False

    def clickMap(self) -> bool:
        """
        打开小地图
        :return:
        """
        return False

    def isInMapWindow(self, img : numpy.array)-> bool:
        """
        是否已经打开小地图
        :param img:
        :return:
        """
        return False

