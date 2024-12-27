import numpy


class FlashBattleDetect:
    def isFlashBattle(self) -> bool:
        """
        判断是否快闪表演
        :return:
        """
        return False

    def isSkipFormation(self) -> bool:
        """
        判断是否跳过编队
        :return:
        """
        return False

    def isInSuccessFlashBattleWindow(self)->bool :
        """
        快闪战斗胜利
        :return:
        """
        return False

    def isInFailedFlashBattleWindow(self)->bool :
        """
        快闪战斗失败
        :return:
        """
        return False

    def isInBattleResultWindow(self)->bool :
        """
        是否打开了演出结算窗口
        :return:
        """
        return False