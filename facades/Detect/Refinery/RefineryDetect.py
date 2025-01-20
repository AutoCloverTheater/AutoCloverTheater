import random
from datetime import datetime

from facades.Constant.Constant import IMG_PATH
from facades.Detect.DetectLog import matchResult
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgRead import MyImread
from facades.Img.ImgSearch import imgSearch, imgSearchArea
from facades.Logx.Logx import logx


class RefineryDetect:

    def mathDate(self) -> int:
        """
        计算今天是周几可以打什么矿
        :return:
        """
        # 定义周几的名称
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        # 获取当前日期
        today = datetime.today()

        # 获取周几的名称
        weekday_name = weekdays[today.weekday()]
        logx.info(f"今天是:{weekday_name}")
        return today.weekday()

    def returnRefineryRoi(self):
        """
        返回矿厂位置
        todo 以后增加一个配置周日打什么矿，没有指定的话就随机打一矿
        :return:
        """
        weekday = datetime.today().weekday()
        refineryRoi = [
            [124, 93, 26, 25],
            [124, 188, 16, 14],
            [126, 268, 20, 20],
            [134, 359, 27, 25],
            [143 ,445 ,15 ,18],
            [138, 536, 18, 24]
        ]
        if weekday == 6:
            index = random.randint(0, 6)
        else:
            index = weekday
        roi = refineryRoi[index]

        res = (roi[0], roi[1])
        return  res

    @matchResult
    def hasAdventureButton(self):
        """
        主页冒险按钮
        :return:
        """
        path = IMG_PATH.joinpath("Main/adventure/adventure__773_622_65_86__723_572_165_148.png")
        img = MyImread(path)
        pots, ok  = imgSearchArea(GetSnapShot().img, img, [723, 572, 165, 148])
        if not ok:
            pots = [(0,0)]
        return {"name":"主页冒险按钮","pot":pots.pop()},ok

    @matchResult
    def isInAdventureListWindow(self):
        """
        冒险之旅
        :return:
        """
        path = IMG_PATH.joinpath("Main/adventure/adventureList__96_23_93_22__46_0_193_95.png")
        mainWindow = MyImread(path)
        pots, ok  = imgSearchArea(GetSnapShot().img, mainWindow, [96, 23, 93, 22])
        if not ok:
            pots = [(0,0)]
        return {"name":"冒险之旅","pot":pots.pop()},ok

    @matchResult
    def hasRefineryEntrance(self):
        """
        页面上是否存在神秘矿厂入口
        :return:
        """
        path = IMG_PATH.joinpath("Main/refinery/refineryEntrance__944_408_302_172__894_358_386_272.png")
        mainWindow = MyImread(path)
        pots, ok  = imgSearchArea(GetSnapShot().img, mainWindow, [944, 408, 302, 172])
        if not ok:
            pots = [(0,0)]
        return {"name":"神秘矿厂入口","pot":pots.pop()},ok

    @matchResult
    def isSwipToEnd(self):
        path = IMG_PATH.joinpath("Main/adventure/sweetDate.png")
        mainWindow = MyImread(path)
        pots, ok  = imgSearchArea(GetSnapShot().img, mainWindow, [918, 438, 307, 128])
        if not ok:
            pots = [(0,0)]
        return {"name":"滑到底了","pot":pots.pop()},ok

    @matchResult
    def isInRefinery(self):
        """
        在神秘矿厂中
        :return:
        """
        path = IMG_PATH.joinpath("Main/refinery/inRefinery__96_22_93_23__46_0_193_95.png")
        img = MyImread(path)
        pots, ok  = imgSearchArea(GetSnapShot().img, img, [96, 22, 93, 23])
        if not ok:
            pots = [(0,0)]
        return {"name":"神秘矿厂","pot":pots.pop()},ok

    @matchResult
    def isCloseFastFormation(self):
        """
        快速编队未开启
        :return:
        """
        path = IMG_PATH.joinpath("Main/refinery/shipFormation__1098_640_118_30__1048_590_218_130.png")
        img = MyImread(path)
        pots, ok  = imgSearchArea(GetSnapShot().img, img, [1098, 640, 118, 30])
        if not ok:
            pots = [(0,0)]
        return {"name":"神秘矿厂-快速编队未开启","pot":pots.pop()},ok

    @matchResult
    def fastBattle(self):
        """
        识别可快闪的矿场
        :return:
        """
        ""
        imgs = [
            "f3__1138_507_56_78__1088_457_156_178.png",
            "f2__1137_332_56_77__1087_282_156_177.png",
            "f1__1138_155_56_78__1088_105_156_178.png",
        ]
        roi = [
            [1135, 495, 63, 94],
            [1136, 317, 65, 97],
            [1136, 146, 66, 91],
        ]

        key = 0
        pot = (0,0)
        ok = False
        for k,v in enumerate(imgs):
            path = IMG_PATH.joinpath(f"Main/refinery/{imgs[k]}")
            img = MyImread(path)
            pots, ok  = imgSearchArea(GetSnapShot().img, img, roi[k], 0.9)
            if ok:
                pot = pots[0]
                key = k
                ok = True
                break

        return {"name":f"识别可快闪的矿场阶段{len(imgs) - key}","pot":pot},ok

    @matchResult
    def isZeroCountForToday(self):
        """
        今日次数是否用光
        :return:
        """
        path = IMG_PATH.joinpath("Main/refinery/zeroCountForToday__1065_17_154_19__1015_0_254_86.png")
        img = MyImread(path)
        pots, ok  = imgSearchArea(GetSnapShot().img, img, [1065, 17, 154, 19], 0.99)
        if not ok:
            pots = [(0,0)]
        return {"name":"今日次数已用光","pot":pots.pop()},ok