import numpy

from facades.Constant.Constant import IMG_PATH
from facades.Detect.DetectLog import matchResult
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgRead import MyImread
from facades.Img.ImgSearch import imgSearchArea, imgSearch
from facades.Logx.Logx import logx


class RelicDetect:

    def __init__(self):
        """
        遗迹
        """
        pass

    @matchResult
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

    @matchResult
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

    @matchResult
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

    @matchResult
    def hasGoExplore(self):
        """
        前往探索
        :return:[]roi
        :return:bool
        """
        path = IMG_PATH.joinpath("main/relic/goExplore__999_612_106_29__949_562_206_129.png")
        img = MyImread(path)
        pot,ok = imgSearchArea(GetSnapShot().img, img, [999, 612, 106, 29])
        if ok:
            pot = pot[0]

        return {"name": "前往探索", "pot": pot}, ok

    @matchResult
    def hasConfirmButton(self):
        """
        确认按钮
        :return:[]roi
        :return:bool
        """
        path = IMG_PATH.joinpath("main/relic/confirm01__618_558_67_30__568_508_167_130.png")
        img = MyImread(path)
        pot,ok = imgSearchArea(GetSnapShot().img, img, [618, 558, 67, 30])
        if ok :
            pot = pot[0]

        return {"name": "确认", "pot": pot}, ok

    @matchResult
    def hasSelectButton(self):
        """
        选择按钮
        :return:
        """
        path = IMG_PATH.joinpath("main/relic/select.png")
        img = MyImread(path)
        pot,ok = imgSearchArea(GetSnapShot().img, img, [926,194,138,270])
        if ok :
            logx.info(f"匹配结果 {pot}")
            pot = pot.pop()

        return {"name": "选择", "pot": pot}, ok

    @matchResult
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
            'red.png',
            'green.png',
            'boss.png',
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
        pot = ()
        name = "未知图标"
        for k,v in enumerate(imgs):
            loading = MyImread(IMG_PATH.joinpath(f"Main/relic/{v}"))
            resp, ok  = imgSearch(GetSnapShot().img, loading, 0.98)
            if ok:
                name = names[k]
                pot = resp
                break

        return {"name": name, "pot": pot}, ok

    def isInRelicGame(self):
        """
        是否在遗迹探索游戏内
        Returns:
        """
        path = "main/relic/location__40_231_41_62__0_181_131_162.png"
        path = IMG_PATH.joinpath(path)
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot().img, img, [40, 231, 41, 62])
        if len(rois) > 0:
            pot = rois[0]
        else:
            pot = (0,0)
        return {"name": "遗迹探索中...", "pot": pot}, ok


    @matchResult
    def location(self):
        """
        重制视角
        Returns:

        """
        path = IMG_PATH.joinpath("main/relic/location__40_231_41_62__0_181_131_162.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot().img, img, [40, 231, 41, 62])
        if len(rois) > 0:
            pot = rois[0]
        else:
            pot = (0,0)

        return {"name": "重制视角", "pot": pot}, ok

    @matchResult
    def hasSettingMap(self):
        """
        选择地图
        Returns:

        """
        maps = [
            "沙漠星城"
        ]

        path = IMG_PATH.joinpath("main/relic/desert__138_205_108_40__88_155_208_140.png")
        img = MyImread(path)
        pot,ok = imgSearchArea(GetSnapShot().img, img, [138, 205, 108, 40])
        if ok:
            pot = pot[0]

        return {"name": f"选择地图 {maps[0]}", "pot": pot}, ok

    @matchResult
    def hasSettingRank(self):
        """
        选择难度
        :return:
        """
        ranks = [
            "普通"
        ]

        path = IMG_PATH.joinpath("main/relic/normal__352_105_97_25__302_55_197_125.png")
        img = MyImread(path)
        pot,ok = imgSearchArea(GetSnapShot().img, img, [352, 105, 97, 25])
        if ok:
            pot = pot[0]

        return {"name": f"选择难度 {ranks[0]}", "pot": pot}, ok

    @matchResult
    def getItems(self):
        """
        获取道具
        :return:
        """
        path = IMG_PATH.joinpath("main/relic/getItems__497_78_282_72__447_28_382_172.png")
        img = MyImread(path)
        pot,ok = imgSearchArea(GetSnapShot().img, img, [497, 78, 282, 72])
        if ok > 0:
            pot = (0.5, 0.0)

        return {"name": "获取道具", "pot": pot}, ok