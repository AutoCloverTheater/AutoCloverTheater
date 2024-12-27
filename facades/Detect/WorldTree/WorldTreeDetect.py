import numpy

from facades.Detect.WorldTree.SelectWindow import WorldTreeSelectWindow

"""
世界树，死境难度。
避战流派只打奇遇而且只会选第一个选项
"""
class WorldTreeDetect:
    dew = 0 # 露水数量
    subWindow = WorldTreeSelectWindow
    def __init__(self):
        self.subWindow = WorldTreeSelectWindow()
        # 初始化所需要的模板文件

    def isInWorldTreeMainWindow(self):
        """
        在世界树探索bata2.0页面
        :return:
        """
        return False

    def isInWorldTreeLeverSelectWindow(self):
        """
        选择难度
        :return:
        """
        pass

    def getLever(self):
        """
        获取当前世界树等级
        :return:
        """
        return 0

    def updateDew(self):
        """
        更新露水数量
        :return:
        """
        return 0

    def hasBizarreCard(self) -> bool:
        """
        是否存在奇遇卡片可选
        :return:
        """
        return False

    def hasRabbitShopCard(self, img : numpy.array) -> bool:
        """
        是否存在兔子商店卡
        :return:
        """
        return False

    def hasDivinationRoomCard(self, img : numpy.array) -> bool:
        """
        是否存在占卜
        :return:
        """
        return False

    def hasTreasureBoxCard(self, img : numpy.array) -> bool:
        """
        是否存在宝箱
        :return:
        """
        return False

    def hasRelaxCard(self) -> bool:
        """
        是否存在休息卡
        :return:
        """
        return False

    def hasEliteBattleCard(self) -> bool:
        """
        是否存在精英战卡
        :return:
        """
        return False

    def hasBattleCard(self) -> bool:
        """
        是否存在战斗卡
        :return:
        """
        return False

    def isInWorldTreeEndWindow(self)->bool :
        """
        世界树探索结束窗口
        :return:
        """
        return False

    def isInWorldTreeBattleReadyWindow(self):
        """
        世界树探索战斗准备窗口
        :return:
        """
        pass