import numpy

from facades.Constant.Constant import IMG_PATH
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgRead import MyImread
from facades.Img.ImgSearch import imgSearchArea, imgSearch


class RelicDetect:

    def __init__(self):
        """
        遗迹
        """
        pass

    def isInRelicEntrance(self):
        """
        遗迹探索准备窗口
        :return:[]roi
        :return:bool
        """
        path = IMG_PATH.joinpath("main/relic/relicEntrance__95_23_91_22__45_0_191_95.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot().img, img, [95, 23, 91, 22])
        if len(rois) > 0:
            pot = rois[0]
        else:
            pot = (0,0)

        return {"name": "遗迹探索", "pot": pot}, ok

    def hasDesert(self):
        """
        是否处于沙漠星城
        :return:[]roi
        :return:bool
        """
        path = IMG_PATH.joinpath("main/relic/desert__138_205_108_40__88_155_208_140.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot().img, img, [138, 205, 108, 40])
        if len(rois) > 0:
            pot = rois[0]
        else:
            pot = (0,0)

        return {"name": "沙漠星城", "pot": pot}, ok

    def hasNormal(self):
        """
        普通难度
        :return:[]roi
        :return:bool
        """
        path = IMG_PATH.joinpath("main/relic/normal__352_105_97_25__302_55_197_125.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot().img, img, [138, 205, 108, 40])
        if len(rois) > 0:
            pot = rois[0]
        else:
            pot = (0,0)

        return {"name": "普通难度", "pot": pot}, ok

    def hasGoExplore(self):
        """
        前往探索
        :return:[]roi
        :return:bool
        """
        path = IMG_PATH.joinpath("main/relic/goExplore__999_612_106_29__949_562_206_129.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot().img, img, [138, 205, 108, 40])
        if len(rois) > 0:
            pot = rois[0]
        else:
            pot = (0,0)

        return {"name": "前往探索", "pot": pot}, ok

    def hasComfirmButton(self):
        """
        确认按钮
        :return:[]roi
        :return:bool
        """
        path = IMG_PATH.joinpath("main/relic/confirm01__618_558_67_30__568_508_167_130..png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot().img, img, [138, 205, 108, 40])
        if len(rois) > 0:
            pot = rois[0]
        else:
            pot = (0,0)

        return {"name": "确认", "pot": pot}, ok

    def pressAnyKeyToContinue(self):
        """
        点击弹窗其他区域关闭
        :return:[]roi
        :return:bool
        """

        imgs = [
            'lag/lag__622_345_35_31__572_295_135_131.png',
            'lag/lag__576_400_136_35__526_350_236_135.png',
            'lag/loading__867_579_343_97__817_529_443_191.png',
        ]
        roi = [
            (622, 345, 35, 31),
            (576, 400, 136, 35),
            (867, 579, 343, 97),
        ]
        ok = False
        pot = (0, 0)

        for k, i in enumerate(imgs):
            loading = MyImread(IMG_PATH.joinpath("lag").joinpath(i))
            resp, ok  = imgSearchArea(GetSnapShot().img, loading, roi[k])
            if ok:
                pot = resp[0]
                break

        return {"name": "点击弹窗其他区域关闭", "pot": pot}, ok

    def  eventPoint(self):
        """
        节点
        :return:[]roi
        :return:bool
        """
        imgs = [
            'blue.png',
            'green.png',
            'red__366_100_69_22__316_50_169_122.png',
            'boos.png',
            'exit.png',
        ]
        names = [
            "跳楼减价",
            "吐血甩卖",
            "奇遇事件",
            "首领怪物",
            "传送门",
        ]

        ok = False
        pot = (0, 0)
        name = "未知图标"
        for k,v in enumerate(imgs):
            loading = MyImread(IMG_PATH.joinpath(f"Main/relic/{v}"))
            resp, ok  = imgSearch(GetSnapShot().img, loading, 0.98)
            if ok:
                name = names[k]
                pot = resp[0]
                break

        return {"name": name, "pot": pot}, ok

    def isInRelicGame(self):
        """
        是否在遗迹探索游戏内
        Returns:
        """
        path = IMG_PATH.joinpath("main/relic/location__40_231_41_62__0_181_131_162.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot().img, img, [40, 231, 41, 62])
        if len(rois) > 0:
            pot = rois[0]
        else:
            pot = (0,0)

        return {"name": "遗迹探索中", "pot": pot}, ok


    def location(self):
        """
        回到当前位置
        Returns:

        """
        path = IMG_PATH.joinpath("main/relic/location__40_231_41_62__0_181_131_162.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot().img, img, [40, 231, 41, 62])
        if len(rois) > 0:
            pot = rois[0]
        else:
            pot = (0,0)

        return {"name": "当前", "pot": pot}, ok