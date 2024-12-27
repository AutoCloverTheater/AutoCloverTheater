import cv2
import numpy


class AdventureDetect:
    def isInAdventure(self, img : numpy.array):
        needLogin = cv2.imread("")
        # 将源图像转换为灰度图像
        img_gray = cv2.cvtColor(needLogin, cv2.COLOR_BGR2GRAY)
        _, max_val, _, _  = cv2.minMaxLoc(cv2.matchTemplate(img, img_gray, cv2.TM_CCOEFF_NORMED))

        # 设置阈值
        threshold = 0.8  # 根据实际情况调整阈值
        if max_val < threshold:
            return False
        return True

    def getAdventureList(self, img : numpy.array):
        """
            获取当前冒险列表
                        是否处于素材准备界面

            Returns:[string]
        """
        needLogin = cv2.imread("")
        # 将源图像转换为灰度图像
        img_gray = cv2.cvtColor(needLogin, cv2.COLOR_BGR2GRAY)
        # 只去识别x-y行的字体
        return []

    def isInsucai(self,img : numpy.array):
        """
            是否处于素材准备界面

            Returns:bool
        """
        needLogin = cv2.imread("")
        # 将源图像转换为灰度图像
        img_gray = cv2.cvtColor(needLogin, cv2.COLOR_BGR2GRAY)
        _, max_val, _, _  = cv2.minMaxLoc(cv2.matchTemplate(img, img_gray, cv2.TM_CCOEFF_NORMED))

        # 设置阈值
        threshold = 0.8  # 根据实际情况调整阈值
        if max_val < threshold:
            return False
        return True

    def isInkuangchang(self,img : numpy.array):
        """
            是否处于矿厂准备界面

            Returns:bool
        """
        needLogin = cv2.imread("")
        # 将源图像转换为灰度图像
        img_gray = cv2.cvtColor(needLogin, cv2.COLOR_BGR2GRAY)
        _, max_val, _, _  = cv2.minMaxLoc(cv2.matchTemplate(img, img_gray, cv2.TM_CCOEFF_NORMED))

        # 设置阈值
        threshold = 0.8  # 根据实际情况调整阈值
        if max_val < threshold:
            return False
        return True

    def isInyijitansuo(self,img : numpy.array):
        """
            是否处于遗迹探索准备界面

            Returns:bool
        """
        needLogin = cv2.imread("")
        # 将源图像转换为灰度图像
        img_gray = cv2.cvtColor(needLogin, cv2.COLOR_BGR2GRAY)
        _, max_val, _, _  = cv2.minMaxLoc(cv2.matchTemplate(img, img_gray, cv2.TM_CCOEFF_NORMED))

        # 设置阈值
        threshold = 0.8  # 根据实际情况调整阈值
        if max_val < threshold:
            return False
        return True

    def inInWorldTree(self,img : numpy.array):
        """
            是否处于世界树准备界面

            Returns:bool
        """
        needLogin = cv2.imread("")
        # 将源图像转换为灰度图像
        img_gray = cv2.cvtColor(needLogin, cv2.COLOR_BGR2GRAY)
        _, max_val, _, _  = cv2.minMaxLoc(cv2.matchTemplate(img, img_gray, cv2.TM_CCOEFF_NORMED))

        # 设置阈值
        threshold = 0.8  # 根据实际情况调整阈值
        if max_val < threshold:
            return False
        return True

    def isClickReadyAdventure(self,img : numpy.array):
        """
            是否点击了出发冒险.

            Returns:bool
        """
        needLogin = cv2.imread("")
        # 将源图像转换为灰度图像
        img_gray = cv2.cvtColor(needLogin, cv2.COLOR_BGR2GRAY)
        _, max_val, _, _  = cv2.minMaxLoc(cv2.matchTemplate(img, img_gray, cv2.TM_CCOEFF_NORMED))

        # 设置阈值
        threshold = 0.8  # 根据实际情况调整阈值
        if max_val < threshold:
            return False
        return True

