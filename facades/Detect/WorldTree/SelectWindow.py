import numpy


class WorldTreeSelectWindow:
    def __init__(self):
        #初始化所需要的模板文件
        pass
    """
    世界树二级页面
    """
    def isInSelectYourArtifact(self, img : numpy.array) -> bool:
        """
        是否在选神器界面
        :return:
        """
        return False

    def isInEventNeedDew(self, img : numpy.array) -> bool:
        """
        遭遇事件需要打水
        1.露水大于x
        2.不喝了
        :return:
        """
        return False

    def isInSelectGift(self) -> bool:
        """
        选择赠礼
        1 远见
        2 友爱
        3 生存
        :param img:
        :return:
        """
        return False

    def isInSelectYourBlessing(self, img : numpy.array):
        """
        选择你的祝福
        1 提升4点速度降低5%防御
        2 获得50点露水
        3 回复6%生命2会合降低10%暴伤
        4 提升1.5%攻防生命
        :param img:
        :return:
        """
        return False

    def isInRabbitShopWindow(self, img : numpy.array) -> bool:
        """
        是否打开了兔子商店窗口
        :return:
        """
        return False

    def isInEncounteredEvent(self, img : numpy.array) -> bool:
        """
        是否打开了遭遇事件窗口
        :return:
        """
        return False