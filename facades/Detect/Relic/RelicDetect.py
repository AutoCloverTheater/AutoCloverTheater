import cv2
import numpy as np
from PIL import ImageEnhance, Image

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
        pot,ok = imgSearchArea(GetSnapShot().img, img, [618,558,67,30])
        if ok :
            pot = pot.pop()

        return {"name": "确认", "pot": pot}, ok

    @matchResult
    def hasSelectButton(self):
        """
        选择按钮
        :return:
        """
        rois = [
            [969,322,51,27],# 第二个选择
            [969,219,50,24],# 第一个选择
        ]

        pot = ()
        ok = False
        for k, roi in enumerate(rois):
            path = IMG_PATH.joinpath("main/relic/select.png")
            img = MyImread(path)
            pot,ok = imgSearchArea(GetSnapShot().img, img, roi)
            if ok :
                logx.info(f"选择按钮{k}")
                pot = (roi[0] + roi[2] / 2,roi[1]+ roi[3] / 2)
                break

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
    @matchResult
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
            "relicExit.png"
        ]
        names = [
            "跳楼减价",
            "吐血甩卖",
            "奇遇事件",
            "首领怪物",
            "传送门",
            "离开"
        ]

        # 降低亮度
        image = GetSnapShot().img

        # 将图片转换为灰度图（计算亮度）
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 定义亮度阈值（0-255，值越小，变黑的部分越多）
        brightness_threshold = 100

        # 创建一个黑色掩码（亮度低于阈值的部分）
        mask = gray < brightness_threshold

        # 将亮度低的部分设置为黑色
        image[mask] = [0, 0, 0]
        darkened_image = image
        # cv2.imwrite("d.png", darkened_image)

        ok = False
        pot = ()
        name = "未知图标"
        for k,v in enumerate(imgs):
            loading = MyImread(IMG_PATH.joinpath(f"Main/relic/{v}"))
            resp, ok  = imgSearch(darkened_image, loading, 0.9)
            if ok:
                name = names[k]
                pot = resp
                break

        return {"name": name, "pot": pot}, ok

    @matchResult
    def isInRelicGame(self):
        """
        是否在遗迹探索游戏内
        Returns:
        """
        path = "Main/relic/location__40_231_41_62__0_181_131_162.png"
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
        path = IMG_PATH.joinpath("Main/relic/location__40_231_41_62__0_181_131_162.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot().img, img, [40, 231, 41, 62])
        if len(rois) > 0:
            pot = rois[0]
        else:
            pot = (0,0)

        return {"name": "重制视角", "pot": pot}, ok

    @matchResult
    def killedBoss(self):
        """
        击杀过boss了
        Returns:
        """
        imgs = [
            "killBoss02__163_45_16_17__113_0_116_112.png",
            "killedBoss__163_45_15_16__113_0_115_111.png",
            "killedBoss03__92_53_47_34__42_3_147_134.png",
        ]
        pot = ()
        ok = False
        for i in imgs:
            path = IMG_PATH.joinpath(f"Main/relic/{i}")
            img = MyImread(path)
            rois,ok = imgSearchArea(GetSnapShot().img, img, [91,40,91,48])
            if ok:
                pot = (703,210)
                break

        return {"name": "击杀过boss了", "pot": pot}, ok

    @matchResult
    def reLocation(self):
        path = IMG_PATH.joinpath("Main/relic/reLocation__701_266_120_26__651_216_220_126.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot().img, img, [690,251,150,126])

        pot = ()
        if ok > 0:
            pot = rois.pop()

        return {"name": "当前路径不能直接跳转请重新选择", "pot": pot}, ok

    @matchResult
    def explorationEnds(self):
        """
        探索结束
        :return:
        """
        path = IMG_PATH.joinpath("Main/relic/explorationEnds__451_122_376_53__401_72_476_153.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot().img, img, [451, 122, 376, 53])
        if len(rois) > 0:
            pot = (0.5, 0)
        else:
            pot = (0,0)

        return {"name": "探索结束", "pot": pot}, ok

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